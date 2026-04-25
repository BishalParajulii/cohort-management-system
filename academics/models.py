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
        return f"{self.name} ({self.department.name} - {self.grade.class_level})"


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
    roll_number = models.IntegerField(blank=True, null=True)
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

    def save(self, *args, **kwargs):
        if not self.roll_number:
            # Get the current maximum roll number for this cohort
            max_roll = Enrollment.objects.filter(cohort=self.cohort).aggregate(
                models.Max('roll_number')
            )['roll_number__max']
            self.roll_number = (max_roll or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.get_full_name()} — Roll {self.roll_number} ({self.cohort})"



class StudentAttendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = 'present', 'Present'
        ABSENT = 'absent', 'Absent'


    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PRESENT)
    remarks = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('enrollment', 'date')

    def __str__(self):
        return f"{self.enrollment.student.get_full_name()} - {self.date} ({self.status})"


class TeacherAttendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = 'present', 'Present'
        ABSENT = 'absent', 'Absent'
        LEAVE = 'leave', 'On Leave'

    teacher = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='teacher_attendances')
    date = models.DateField()
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PRESENT)
    remarks = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('teacher', 'date')

    def clean(self):
        if self.teacher and not self.teacher.is_teacher():
            raise ValidationError('Only users with the teacher role can have teacher attendance records.')

    def __str__(self):
        return f"{self.teacher.get_full_name()} - {self.date} ({self.status})"

