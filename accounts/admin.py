from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, StudentProfile, TeacherProfile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Add your custom fields to the admin forms
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Roles & Info', {'fields': ('role', 'phone', 'address')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Roles & Info', {'fields': ('role', 'phone', 'address')}),
    )
    list_display = ('username', 'email', 'role', 'is_staff')

admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
