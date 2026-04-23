from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, StudentProfile, TeacherProfile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Add your custom fields to the admin forms
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Roles & Info', {'fields': ('role', 'phone')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Roles & Info', {'fields': ('role', 'phone')}),
    )
    list_display = ('username', 'email', 'role', 'is_staff')

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'guardian_name', 'guardian_phone')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(role=User.Role.STUDENT)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'joining_date')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(role=User.Role.TEACHER)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
