from django.contrib import admin
from .models import Subject, Enrollment, StudentAttendance, TeacherAttendance, AcademicResult
from accounts.models import User


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department', 'grade', 'credit_hours')
    list_filter = ('department', 'grade')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'cohort', 'roll_number', 'status', 'enrolled_date')
    list_filter = ('status', 'cohort__academic_year', 'cohort__section__department')
    filter_horizontal = ('subjects',)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            kwargs["queryset"] = User.objects.filter(role=User.Role.STUDENT)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'date', 'status')
    list_filter = ('status', 'date')


@admin.register(TeacherAttendance)
class TeacherAttendanceAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'date', 'status')
    list_filter = ('status', 'date')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            kwargs["queryset"] = User.objects.filter(role=User.Role.TEACHER)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(AcademicResult)
class AcademicResultAdmin(admin.ModelAdmin):
    list_display = (
        'enrollment', 'student_name', 'subject', 'term',
        'marks_obtained', 'max_marks', 'grade'
    )
    list_filter = (
        'term',
        'subject__department',
        'enrollment__cohort__section__grade',
        'enrollment__cohort__section__department',
    )
    search_fields = (
        'enrollment__student__username',
        'enrollment__student__first_name',
        'enrollment__student__last_name',
        'subject__name',
    )

    def student_name(self, obj):
        return obj.enrollment.student.get_full_name()
    student_name.short_description = 'Student'
