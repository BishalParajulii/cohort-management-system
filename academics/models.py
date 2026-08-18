from decimal import Decimal

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

    def clean(self):
        if self.teacher and not self.teacher.is_teacher():
            raise ValidationError('Only users with the teacher role can have teacher attendance records.')

    def __str__(self):
        return f"{self.teacher.get_full_name()} - {self.date} ({self.status})"


class AcademicResult(models.Model):
    class Term(models.TextChoices):
        FIRST_TERM = 'first_term', 'First Term'
        SECOND_TERM = 'second_term', 'Second Term'
        BOARD_EXAM = 'board_exam', 'Board Exam'

    enrollment = models.ForeignKey(
        Enrollment, on_delete=models.CASCADE, related_name='results'
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name='results'
    )
    term = models.CharField(max_length=20, choices=Term.choices)
    marks_obtained = models.DecimalField(max_digits=6, decimal_places=2)
    max_marks = models.PositiveIntegerField(default=100)
    grade = models.CharField(max_length=10, blank=True, null=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('enrollment', 'subject', 'term')
        ordering = ['enrollment', 'term', 'subject']

    GRADE_POINT_SCALE = [
        (Decimal('90.0'), 'A+', Decimal('4.0')),
        (Decimal('80.0'), 'A', Decimal('4.0')),
        (Decimal('75.0'), 'B+', Decimal('3.5')),
        (Decimal('70.0'), 'B', Decimal('3.0')),
        (Decimal('65.0'), 'C+', Decimal('2.5')),
        (Decimal('60.0'), 'C', Decimal('2.0')),
        (Decimal('50.0'), 'D', Decimal('1.0')),
        (Decimal('0.0'), 'F', Decimal('0.0')),
    ]

    def clean(self):
        if self.enrollment and not self.enrollment.student.is_student():
            raise ValidationError('Results can only be recorded for student enrollments.')
        if self.subject and self.enrollment and self.subject.grade != self.enrollment.cohort.section.grade:
            raise ValidationError('Subject grade must match the student enrollment class.')

    @property
    def percentage(self):
        if self.max_marks:
            percentage = (Decimal(self.marks_obtained) / Decimal(self.max_marks)) * Decimal('100')
            return percentage.quantize(Decimal('0.01'))
        return None

    @property
    def grade_letter(self):
        if self.grade:
            return self.grade
        percentage = self.percentage
        if percentage is None:
            return None
        for threshold, letter, _ in self.GRADE_POINT_SCALE:
            if percentage >= threshold:
                return letter
        return 'F'

    @property
    def grade_point(self):
        percentage = self.percentage
        if percentage is None:
            return None
        for threshold, _, point in self.GRADE_POINT_SCALE:
            if percentage >= threshold:
                return point
        return Decimal('0.0')

    @property
    def weighted_points(self):
        if self.grade_point is None:
            return None
        return (self.grade_point * Decimal(self.subject.credit_hours)).quantize(Decimal('0.01'))

    @staticmethod
    def calculate_gpa(results):
        total_credit = Decimal('0.0')
        total_weighted = Decimal('0.0')
        for result in results:
            if result.grade_point is None:
                continue
            total_credit += Decimal(result.subject.credit_hours)
            total_weighted += result.weighted_points
        if total_credit == 0:
            return None
        return (total_weighted / total_credit).quantize(Decimal('0.01'))

    def __str__(self):
        return f"{self.enrollment.student.get_full_name()} - {self.subject.name} ({self.term})"

