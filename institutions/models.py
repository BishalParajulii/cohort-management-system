from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Institution(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    logo = models.ImageField(upload_to='logo/' , blank=True)
    
    def __str__(self):
        return self.name



class Department(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE , related_name='departments')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    head = models.ForeignKey('accounts.User', on_delete=models.SET_NULL , null=True , blank=True,related_name='departments')

    class Meta:
        unique_together = ('institution', 'name')

    
    def __str__(self):
        return f"{self.name} ({self.institution.name})"


class AcademicYear(models.Model):
    """Tracks academic sessions — e.g. 2081-2082"""
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='academic_years')
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ('institution', 'name')
        ordering = ['-start_date']

    def clean(self):
        if self.start_date and self.end_date and self.start_date >= self.end_date:
            raise ValidationError('Start date must be before end date.')

    def __str__(self):
        return f"{self.name} ({self.institution.name})"


class Grade(models.Model):
    """Class levels — Class 11, Class 12"""
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='grades')
    name = models.CharField(max_length=50)
    order = models.IntegerField(default=0)

    class Meta:
        unique_together = ('institution', 'name')
        ordering = ['order']

    def __str__(self):
        return self.name


class Shift(models.Model):
    """Morning, Day shift"""
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='shifts')
    name = models.CharField(max_length=50)

    class Meta:
        unique_together = ('institution', 'name')

    def __str__(self):
        return self.name


class Section(models.Model):
    """A section within department + grade + shift.
    E.g. Science Class 11 Morning — Section A
    """
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
