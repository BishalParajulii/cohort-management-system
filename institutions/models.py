from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Institution(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    logo = models.ImageField(upload_to='logo/' , blank=True)
    
    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=20, unique=True)
    head = models.ForeignKey('accounts.User', on_delete=models.SET_NULL , null=True , blank=True,related_name='departments')

    def __str__(self):
        return self.name


class AcademicYear(models.Model):

    name = models.CharField(max_length=50, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_date']

    def clean(self):
        if self.start_date and self.end_date and self.start_date >= self.end_date:
            raise ValidationError('Start date must be before end date.')

    def __str__(self):
        return self.name


class Grade(models.Model):
    name = models.CharField(max_length=50, unique=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Shift(models.Model):
    
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Section(models.Model):

    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='sections')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='sections')
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=10)

    class Meta:
        unique_together = ('department', 'grade', 'shift', 'name')

    def __str__(self):
        return f"{self.department.name} {self.grade.name} - Sec {self.name} ({self.shift.name})"


class Cohort(models.Model):

    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='cohorts')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='cohorts')
    class_teacher = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='managed_cohorts'
    )

    class Meta:
        unique_together = ('section', 'academic_year')

    def __str__(self):
        return f"{self.section} — {self.academic_year.name}"
