"""conf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from findjob import views as findjobs_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', findjobs_views.main_view, name='main_view'),
    path('vacancies', findjobs_views.all_vacancies, name='all_vacancies'),
    path('vacancies/cat/<str:specialty_input>', findjobs_views.all_vacancies_special, name='all_vacancies_special'),
    path('companies/<int:company_id>', findjobs_views.company_cart, name='company_cart'),
    path('vacancies/<int:vacancy_id>', findjobs_views.vacancy_cart, name='vacancy_cart'),
]
