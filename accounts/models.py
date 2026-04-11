from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        TEACHER = 'teacher' , 'Teacher'
        STUDENT = 'student', 'Student'
        COORDINATOR = 'coordinator', 'Coordinator'
        
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.ADMIN)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    def is_student(self):
        return self.role == self.Role.STUDENT
    
    def is_teacher(self):
        return self.role == self.Role.TEACHER

    def is_admin(self):
        return self.role == self.Role.ADMIN

    def is_coordinator(self):
        return self.role == self.Role.COORDINATOR
    
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , related_name='student_profile')
    guardian_name = models.CharField(max_length=255)
    guardian_phone = models.CharField(max_length=20)
    guardian_relation = models.CharField(max_length=50)
    address = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()}"
    
class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    department = models.ForeignKey(
        'institutions.Department', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='teachers'
    )
    subjects = models.ManyToManyField(
        'academics.Subject', related_name='teachers', blank=True
    )
    joining_date = models.DateField()
    address = models.TextField(blank=True)

    def __str__(self):
        dept = self.department.name if self.department else 'Unassigned'
        return f"{self.user.get_full_name()} — {dept}"