from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    specialty = models.ForeignKey('Specialty', on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='vacancies', default=None, null=True)
    skills = models.CharField(max_length=100)
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField(default=timezone.now)


class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='company')
    description = models.TextField()
    employee_count = models.IntegerField()
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner_company', default=None, null=True)


class Specialty(models.Model):
    code = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='speciality')

    def __str__(self):
        return self.title


class Application(models.Model):
    written_username = models.CharField(max_length=100)
    written_phone = PhoneNumberField(null=False, blank=False, unique=True)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications', null=True)


class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='resume', null=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    salary = models.IntegerField()
    specialty = models.ForeignKey('Specialty', on_delete=models.CASCADE, related_name='resume')
    education = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    portfolio = models.CharField(max_length=100)

    INACTIVE_STATUS = ('1', 'Не ищу работу')
    PASSIVE_STATUS = ('2', 'Рассматриваю предложения')
    ACTIVE_STATUS = ('3', 'Ищу работу')

    STATUS_CHOICES = [
        INACTIVE_STATUS,
        PASSIVE_STATUS,
        ACTIVE_STATUS,
    ]

    TRAINEE_GRADE = ('1', 'Стажер')
    JUNIOR_STATUS = ('2', 'Джуниор')
    MIDDLE_STATUS = ('3', 'Миддл')
    SENIOR_GRADE = ('4', 'Синьор')
    LEAD_GRADE = ('5', 'Лид')

    GRADES_CHOICES = [
        TRAINEE_GRADE,
        JUNIOR_STATUS,
        MIDDLE_STATUS,
        SENIOR_GRADE,
        LEAD_GRADE,
    ]

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=ACTIVE_STATUS)
    grade = models.CharField(max_length=1, choices=GRADES_CHOICES, default=0, null=True)
