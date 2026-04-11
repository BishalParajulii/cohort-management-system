from django.contrib import admin
from .models import Subject, Enrollment


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department', 'grade', 'credit_hours')
    list_filter = ('department', 'grade')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'cohort', 'roll_number', 'status', 'enrolled_date')
    list_filter = ('status', 'cohort__academic_year', 'cohort__section__department')
    filter_horizontal = ('subjects',)
