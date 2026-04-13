from django.contrib import admin
from .models import Institution, Department, AcademicYear, Grade, Shift, Section, Cohort


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'head')


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active',)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('class_level', 'order')


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'department', 'grade', 'shift')
    list_filter = ('department', 'grade', 'shift')


@admin.register(Cohort)
class CohortAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'academic_year', 'class_teacher')
    list_filter = ('academic_year', 'section__department', 'section__grade', 'section__shift')
