from django.db.models import Count
from django.shortcuts import render, get_object_or_404

from findjob.models import Vacancy, Company, Specialty


def main_view(request):
    companies_list = Company.objects.annotate(count=Count('vacancies'))
    specialties_list = Specialty.objects.annotate(count=Count('vacancies'))
    context = {
        'companies_list': companies_list,
        'specialties_list': specialties_list,
    }
    return render(request, 'findjob/index.html', context=context)


def all_vacancies(request):
    vacancies_list = Vacancy.objects.all()
    vacancy_title = 'Все вакансии'
    context = {
        'vacancies_list': vacancies_list,
        'vacancy_title': vacancy_title,
    }
    return render(request, 'findjob/vacancies.html', context=context)


def all_vacancies_special(request, specialty_input: str):
    specialties_list = get_object_or_404(Specialty, code=specialty_input)
    vacancies_list = specialties_list.vacancies.all()
    vacancy_title = specialties_list.title
    context = {
        'vacancies_list': vacancies_list,
        'vacancy_title': vacancy_title,
        'specialties_list': specialties_list,
    }
    return render(request, 'findjob/vacancies.html', context=context)

def company_cart(request, company_id: int):
    companies_list = get_object_or_404(Company, id=company_id)
    vacancies_list = companies_list.vacancies.all()
    context = {
        'companies_list': companies_list,
        'vacancies_list': vacancies_list,
    }
    return render(request, 'findjob/company.html', context=context)


def vacancy_cart(request, vacancy_id: int):
    vacancies_list = get_object_or_404(Vacancy, id=vacancy_id)
    companies_list = Company.objects.get(vacancies__id=vacancy_id)
    context = {
        'vacancies_list': vacancies_list,
        'companies_list': companies_list,
    }
    return render(request, 'findjob/vacancy.html', context=context)
