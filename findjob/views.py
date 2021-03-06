from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Q
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView

from findjob.forms import ApplicationForm, CompanyForm, VacancyForm, ResumeForm
from findjob.models import Vacancy, Company, Specialty, Application, Resume


# _____Main views_____

def main_view(request):
    companies_list = Company.objects.annotate(count=Count('vacancies'))
    specialties_list = Specialty.objects.annotate(count=Count('vacancies'))
    context = {
        'companies_list': companies_list,
        'specialties_list': specialties_list,
    }
    return render(request, 'findjob/main_pages/index.html', context=context)


def all_vacancies(request):
    vacancies_list = Vacancy.objects.all()
    vacancy_title = 'Все вакансии'
    context = {
        'vacancies_list': vacancies_list,
        'vacancy_title': vacancy_title,
    }
    return render(request, 'findjob/main_pages/vacancies.html', context=context)


def all_vacancies_special(request, specialty_input: str):
    specialties_list = get_object_or_404(Specialty, code=specialty_input)
    vacancies_list = specialties_list.vacancies.all()
    vacancy_title = specialties_list.title
    context = {
        'vacancies_list': vacancies_list,
        'vacancy_title': vacancy_title,
        'specialties_list': specialties_list,
    }
    return render(request, 'findjob/main_pages/vacancies.html', context=context)


def company_cart(request, company_id: int):
    companies_list = get_object_or_404(Company, id=company_id)
    vacancies_list = companies_list.vacancies.all()
    context = {
        'companies_list': companies_list,
        'vacancies_list': vacancies_list,
    }
    return render(request, 'findjob/main_pages/company.html', context=context)


def vacancy_cart(request, vacancy_id: int):
    vacancies_list = get_object_or_404(Vacancy, id=vacancy_id)
    context = {
        'vacancies_list': vacancies_list,
        'form': ApplicationForm,
    }
    return render(request, 'findjob/main_pages/vacancy.html', context=context)


def search(request):
    search_query = request.GET.get('search', '')
    if search_query.isalpha():
        found_vacancies = Vacancy.objects.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query) | Q(
                skills__icontains=search_query))
    else:
        found_vacancies = None
    return render(request, 'findjob/main_pages/search.html', context={'found_vacancies': found_vacancies})


# _____For vacancies create/update_____

class VacancyCreateView(CreateView):
    model = Vacancy
    form_class = VacancyForm

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return 'findjob/myvacancies_pages/vacancy-create.html'
        else:
            return 'findjob/main_pages/need_authorization.html'

    def form_valid(self, form):
        vacancy_form = form.save(commit=False)
        vacancy_form.save()
        the_vacancy = Vacancy.objects.get(pk=vacancy_form.pk)
        the_company = Company.objects.get(owner=self.request.user)
        the_vacancy.company = the_company
        the_vacancy.save()
        return redirect('/mycompany/vacancies')


class VacancyListView(ListView):
    context_object_name = 'vacancy_list'

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return 'findjob/myvacancies_pages/vacancy-list.html'
        else:
            return 'findjob/main_pages/need_authorization.html'

    def get_queryset(self):
        try:
            user = self.request.user
            company = get_object_or_404(Company, owner=user)
        except:
            return None
        else:
            return Vacancy.objects.filter(company=company.id)


class VacancyEditView(SuccessMessageMixin, UpdateView):
    form_class = VacancyForm
    success_message = 'Информация о вакансии обновлена'
    template_name = 'findjob/myvacancies_pages/vacancy-edit.html'
    success_url = reverse_lazy('mycompany_vacancies')
    context_object_name = 'vacancy_list'

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return 'findjob/myvacancies_pages/vacancy-edit.html'
        else:
            return 'findjob/main_pages/need_authorization.html'

    def get_object(self, queryset=None):
        vacancy_id = self.kwargs.get('vacancy_id', None)
        print(vacancy_id)
        vacancy_list = get_object_or_404(Vacancy, id=vacancy_id)
        print(vacancy_list)
        return vacancy_list


# _____For applications create_____

class ApplicationView(View):

    def get(self, request, vacancy_id: int):
        vacancies_list = get_object_or_404(Vacancy, id=vacancy_id)
        companies_list = get_object_or_404(Company, vacancies__id=vacancy_id)
        context = {
            'vacancies_list': vacancies_list,
            'companies_list': companies_list,
            'form': ApplicationForm,
        }
        return render(request, 'findjob/main_pages/vacancy.html', context=context)

    def post(self, request, vacancy_id):
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.vacancy_id = vacancy_id
            application.user_id = request.user.id
            application.save()
            return redirect('vacancy_send', vacancy_id)
        messages.error(request, 'Ошибка в заявке, попробуйте снова')
        return redirect(request.path)


class ApplicationListView(ListView):
    context_object_name = 'applications_list'

    def get_template_names(self):
        if self.request.user.is_authenticated:
            vacancy_id = self.kwargs.get('vacancy_id', None)
            the_vacancy = Vacancy.objects.filter(id=vacancy_id).first()
            print(the_vacancy.id, self.request.user.id)
            the_company = the_vacancy.company
            if the_company.owner.id != self.request.user.id:
                return 'findjob/mycompany_pages/mycompany.html'
            else:
                return 'findjob/myvacancies_pages/applications.html'
        else:
            return 'findjob/main_pages/need_authorization.html'

    def get_queryset(self):
        vacancy_id = self.kwargs.get('vacancy_id', None)
        applications_list = Application.objects.filter(vacancy=vacancy_id)
        return applications_list


class ApplicationResultView(View):

    def get(self, request, vacancy_id):
        return render(request, 'findjob/main_pages/sent.html', {'vacancy_id': vacancy_id})


# _____For company create/update_____

class CompanyCreateView(CreateView):
    model = Company
    form_class = CompanyForm

    def get_template_names(self):
        if self.request.user.is_authenticated:
            try:
                get_object_or_404(Company, owner=self.request.user)
            except:
                return 'findjob/mycompany_pages/company-edit.html'
            else:
                return 'findjob/mycompany_pages/mycompany.html'
        else:
            return 'findjob/main_pages/need_authorization.html'

    def form_valid(self, form):
        company_form = form.save(commit=False)
        company_form.owner = self.request.user
        company_form.save()
        return redirect('/mycompany')


class MycompanyView(SuccessMessageMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    success_message = 'Информация о компании обновлена'
    success_url = reverse_lazy('mycompany')

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return 'findjob/mycompany_pages/mycompany.html'
        else:
            return 'findjob/main_pages/need_authorization.html'

    def get_object(self):
        user = self.request.user
        try:
            object = get_object_or_404(Company, owner=user)
        except:
            object = None
            return object
        else:
            return object


# _____For resume create/update_____

class ResumeCreateView(CreateView):
    model = Resume
    form_class = ResumeForm

    def form_valid(self, form):
        resume_form = form.save(commit=False)
        resume_form.user = self.request.user
        resume_form.save()
        return redirect('/resume')

    def get_template_names(self):
        if self.request.user.is_authenticated:
            try:
                get_object_or_404(Resume, user=self.request.user)
            except:
                return 'findjob/myresume_pages/resume-create.html'
            else:
                return 'findjob/myresume_pages/resume.html'
        else:
            return 'findjob/main_pages/need_authorization.html'


class MyResumeView(SuccessMessageMixin, UpdateView):
    model = Resume
    form_class = ResumeForm
    success_message = 'Резюме обновлено'
    template_name = 'findjob/myresume_pages/resume.html'
    success_url = reverse_lazy('resume')

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return 'findjob/myresume_pages/resume.html'
        else:
            return 'findjob/main_pages/need_authorization.html'

    def get_object(self):
        user = self.request.user
        try:
            object = get_object_or_404(Resume, user=user)
        except:
            object = None
            return object
        else:
            return object


# _____For handlers_____

def custom_handler400(request, exception):
    # Call when SuspiciousOperation raised
    return HttpResponseBadRequest('Неверный запрос!')


def custom_handler403(request, exception):
    # Call when PermissionDenied raised
    return HttpResponseForbidden('Доступ запрещен!')


def custom_handler404(request, exception):
    # Call when Http404 raised
    return HttpResponseNotFound('Ресурс не найден!')


def custom_handler500(request):
    # Call when raised some python exception
    return HttpResponseServerError('Ошибка сервера!')
