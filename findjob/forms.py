from crispy_forms.bootstrap import AppendedText, FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from django import forms

from findjob.models import Application, Vacancy, Company, Resume


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('written_username','written_phone','written_cover_letter')

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['written_username'].label = "Укажите Ваше имя"
        self.fields['written_phone'].label = "Ваш телефон"
        self.fields['written_cover_letter'].label = "Сопроводительное письмо"
        self.helper.form_method = 'post'

        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-4'
        self.helper.layout = Layout(
            Fieldset(
                'Отозваться на вакансию',
                'written_username',
                AppendedText('written_phone', '&#9742;'),
                AppendedText('written_cover_letter', '&#9998;'),

            ),
            FormActions(
                Submit('submit','Отправить заявку')
            )
        )

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name','logo','employee_count','location','description')

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['name'].label = "Название компании"
        self.fields['logo'].label = "Логотип"
        self.fields['employee_count'].label = "Количество человек в компании"
        self.fields['location'].label = "География"
        self.fields['description'].label = "Информация о компании"
        self.helper.form_method = 'post'

        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset(
                'Создать компанию',
                'name',
                'logo',
                'employee_count',
                'location',
                'description',
            ),
            FormActions(
                Submit('submit','Сохранить')
            )
        )

class CompanyEditForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name','logo','employee_count','location','description')
        widgets = {
            'name': forms.TextInput({'class': 'form-control'}),
            'description': forms.TextInput({'class': 'form-control'}),
        }

class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ('title','specialty','skills','description','salary_min','salary_max')

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['title'].label = "Название вакансии"
        self.fields['specialty'].label = "Специализация"
        self.fields['salary_min'].label = "Зарплата от"
        self.fields['salary_max'].label = "Зарплата до"
        self.fields['skills'].label = "Требуемые навыки"
        self.fields['description'].label = "Описание вакансии"
        self.helper.form_method = 'post'

        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset(
                'Создать вакансию',
                'title',
                'specialty',
                'salary_min',
                'salary_max',
                'skills',
                'description',
            ),
            FormActions(
                Submit('submit','Сохранить')
            )
        )

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ('name','surname','salary','specialty','education','experience','portfolio','status','grade')

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['name'].label = "Имя"
        self.fields['surname'].label = "Фамилия"
        self.fields['salary'].label = "Ожидаемое вознаграждение"
        self.fields['specialty'].label = "Специализация"
        self.fields['education'].label = "Образование"
        self.fields['experience'].label = "Опыт работы"
        self.fields['portfolio'].label = "Ссылка на портфолио"
        self.fields['status'].label = "Готовность к работе"
        self.fields['grade'].label = "Квалификация"
        self.helper.form_method = 'post'

        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset(
                'Создать резюме',
                'name',
                'surname',
                'salary',
                'specialty',
                'education',
                'experience',
                'portfolio',
                'status',
                'grade',

            ),
            FormActions(
                Submit('submit','Сохранить')
            )
        )