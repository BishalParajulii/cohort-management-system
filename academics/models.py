from django.db import models
from django.core.exceptions import ValidationError


class Subject(models.Model):

    department = models.ForeignKey(
        'institutions.Department', on_delete=models.CASCADE, related_name='subjects'
    )
    grade = models.ForeignKey(
        'institutions.Grade', on_delete=models.CASCADE, related_name='subjects'
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True, null=True)
    credit_hours = models.IntegerField(default=0)
    

    class Meta:
        unique_together = ('department', 'grade', 'name')

    def __str__(self):
        return f"{self.name} ({self.department.name} - {self.grade.name})"


class Enrollment(models.Model):

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        DROPPED = 'dropped', 'Dropped'
        GRADUATED = 'graduated', 'Graduated'

    student = models.ForeignKey(
        'accounts.User', on_delete=models.CASCADE, related_name='enrollments'
    )
    cohort = models.ForeignKey(
        'institutions.Cohort', on_delete=models.CASCADE, related_name='enrollments'
    )
    roll_number = models.IntegerField()
    subjects = models.ManyToManyField(Subject, related_name='enrollments', blank=True)
    enrolled_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ACTIVE
    )

    class Meta:
        unique_together = [
            ('cohort', 'roll_number'),
            ('student', 'cohort'),
        ]

    def clean(self):
        if self.student and not self.student.is_student():
            raise ValidationError('Only users with the student role can be enrolled.')

    def __str__(self):
        return f"{self.student.get_full_name()} — Roll {self.roll_number} ({self.cohort})"
