from django.contrib import admin
from .models import Vacancy, Company, Specialty, Application
# Register your models here.

class VacancyAdmin(admin.ModelAdmin):
    fields = ('title', 'specialty', 'company', 'skills', 'description', 'salary_min', 'salary_max', 'published_at')
    readonly_fields = ('published_at',)
    pass

class CompanyAdmin(admin.ModelAdmin):
    fields = ('name', 'location', 'logo', 'description', 'employee_count')
    pass

class SpecialtyAdmin(admin.ModelAdmin):
    fields = ('code', 'title', 'picture')
    pass

class ApplicationAdmin(admin.ModelAdmin):
    fields = ('written_username', 'written_phone', 'written_cover_letter', 'vacancy', 'user')
    pass

admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Specialty, SpecialtyAdmin)
admin.site.register(Application, ApplicationAdmin)