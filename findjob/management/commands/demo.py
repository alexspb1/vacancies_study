import json

from django.core.management import BaseCommand

from findjob.models import Vacancy, Company, Specialty

class Command(BaseCommand):
    help = 'Update models'

    def handle(self, *args, **options):

        with open('companies.json', encoding="utf8") as file:
            companies_data = json.load(file)
        for company in companies_data:
            companies = Company.objects.create (
            id = company['id'],
            name = company['title'],
            location = company['location'],
            logo = company['logo'],
            description = company['description'],
            employee_count = company['employee_count'],
        )

        with open('specialties.json', encoding="utf8") as file:
            specialties_data = json.load(file)
        for post in specialties_data:
            specialties = Specialty.objects.create (
            code = post['code'],
            title = post['title'],
        )

        with open('jobs.json', encoding="utf8") as file:
             vacancies_data = json.load(file)
        for vacancy in vacancies_data:
            speciality_from_data = Specialty.objects.get(code=vacancy['specialty'])
            company_from_data = Company.objects.get(id=vacancy['company'])
            vacancies = Vacancy.objects.create (
                title = vacancy['title'],
                specialty = speciality_from_data,
                company = company_from_data,
                skills = vacancy['skills'],
                description = vacancy['description'],
                salary_min = vacancy['salary_from'],
                salary_max = vacancy['salary_to'],
                published_at = vacancy['posted'],
            )