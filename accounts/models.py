from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        TEACHER = 'teacher' , 'Teacher'
        STUDENT = 'student', 'Student'
        coordinator = 'coordinator', 'Coordinator'
        
    role = models.CharField(max_length=20, choices=Role.choices)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    def is_student(self):
        return self.role == self.Role.STUDENT
    
    def is_teacher(self):
        return self.role == self.Role.TEACHER
    
    
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , related_name='student_profile')
    gurdian_name = models.CharField(max_length=255)
    gurdian_phone = models.CharField(max_length=20)
    gurdian_relation = models.CharField(max_length=50)
    address = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()}"
    
class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , related_name='teacher_profile')
    specialization = models.CharField(max_length=255)
    joining_date = models.DateField()
    address = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.specialization}"
    
    