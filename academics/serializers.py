from rest_framework import serializers
from .models import Subject, Enrollment, StudentAttendance, TeacherAttendance, AcademicResult

class SubjectSerializer(serializers.ModelSerializer):
    grade_name = serializers.ReadOnlyField(source='grade.class_level')
    department_name = serializers.ReadOnlyField(source='department.name')

    class Meta:
        model = Subject
        fields = '__all__'
        extra_kwargs = {
            'grade': {'required': True},
            'department': {'required': True}
        }

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'

class StudentAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAttendance
        fields = '__all__'

class TeacherAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAttendance
        fields = '__all__'


class AcademicResultSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source='enrollment.student.get_full_name')
    grade_level = serializers.ReadOnlyField(source='enrollment.cohort.section.grade.class_level')
    section = serializers.ReadOnlyField(source='enrollment.cohort.section.name')
    academic_year = serializers.ReadOnlyField(source='enrollment.cohort.academic_year.name')
    department = serializers.ReadOnlyField(source='enrollment.cohort.section.department.name')
    subject_name = serializers.ReadOnlyField(source='subject.name')
    subject_code = serializers.ReadOnlyField(source='subject.code')
    credit_hours = serializers.ReadOnlyField(source='subject.credit_hours')
    percentage = serializers.ReadOnlyField()
    grade_letter = serializers.ReadOnlyField()
    grade_point = serializers.ReadOnlyField()
    weighted_points = serializers.ReadOnlyField()

    class Meta:
        model = AcademicResult
        fields = [
            'id', 'enrollment', 'student_name', 'subject', 'subject_name',
            'subject_code', 'credit_hours', 'term', 'marks_obtained',
            'max_marks', 'percentage', 'grade', 'grade_letter', 'grade_point',
            'weighted_points', 'remarks', 'grade_level', 'section', 'department',
            'academic_year', 'created_at', 'updated_at'
        ]
