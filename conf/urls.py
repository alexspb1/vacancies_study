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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from findjob import views as findjobs_views
from authorization import views as au_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', findjobs_views.main_view, name='main_view'),
    path('vacancies', findjobs_views.all_vacancies, name='all_vacancies'),
    path('vacancies/cat/<str:specialty_input>', findjobs_views.all_vacancies_special, name='all_vacancies_special'),
    path('companies/<int:company_id>', findjobs_views.company_cart, name='company_cart'),
    path('vacancies/<int:vacancy_id>', findjobs_views.ApplicationView.as_view(), name='vacancy_cart'),
    path('vacancies/<int:vacancy_id>/send', findjobs_views.ApplicationResultView.as_view(), name='vacancy_send'),
    path('mycompany/create', findjobs_views.CompanyCreateView.as_view(), name='mycompany_create'),
    path('mycompany', findjobs_views.MycompanyView.as_view(), name='mycompany'),
    path('mycompany/vacancies', findjobs_views.VacancyListView.as_view(), name='mycompany_vacancies'),
    path('mycompany/vacancies/create', findjobs_views.VacancyCreateView.as_view(), name='mycompany_vacancy_create'),
    path('mycompany/vacancies/<int:vacancy_id>', findjobs_views.VacancyEditView.as_view(), name='mycompany_vacancy_edit'),
    path('mycompany/vacancies/applications/<int:vacancy_id>', findjobs_views.ApplicationListView.as_view(), name='mycompany_application_list'),
    path('resume', findjobs_views.MyResumeView.as_view(), name='resume'),
    path('resume/create', findjobs_views.ResumeCreateView.as_view(), name='resume_create'),
    path('search', findjobs_views.search, name='search'),
    path('login', au_views.MyLoginView.as_view(), name='login_user'),
    path('register', au_views.MySignupView.as_view(), name='register'),
    path('logout', au_views.logout_user, name='logout_user'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

