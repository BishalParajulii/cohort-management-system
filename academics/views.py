from decimal import Decimal

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Subject, Enrollment, StudentAttendance, TeacherAttendance, AcademicResult
from .serializers import (
    SubjectSerializer, EnrollmentSerializer,
    StudentAttendanceSerializer, TeacherAttendanceSerializer,
    AcademicResultSerializer
)
from core.permissions import *

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated, (IsManagement | IsStudentReadOnly)]

    def get_queryset(self):
        qs = Subject.objects.all()
        grade_id = self.request.query_params.get('grade_id')
        grade_level = self.request.query_params.get('grade_level')
        department_id = self.request.query_params.get('department_id')

        if grade_id:
            qs = qs.filter(grade_id=grade_id)
        elif grade_level:
            qs = qs.filter(grade__class_level=grade_level)

        if department_id:
            qs = qs.filter(department_id=department_id)

        return qs

class AcademicResultViewSet(viewsets.ModelViewSet):
    queryset = AcademicResult.objects.all()
    serializer_class = AcademicResultSerializer
    permission_classes = [IsAuthenticated, (IsManagement | IsStudentReadOnly)]

    def get_queryset(self):
        qs = AcademicResult.objects.all()
        user = self.request.user
        student_id = self.request.query_params.get('student_id')
        grade_id = self.request.query_params.get('grade_id')
        grade_level = self.request.query_params.get('grade_level')
        department_id = self.request.query_params.get('department_id')
        term = self.request.query_params.get('term')

        if user.is_authenticated and user.is_student():
            qs = qs.filter(enrollment__student=user)
        elif student_id:
            qs = qs.filter(enrollment__student_id=student_id)

        if grade_id:
            qs = qs.filter(enrollment__cohort__section__grade_id=grade_id)
        elif grade_level:
            qs = qs.filter(enrollment__cohort__section__grade__class_level=grade_level)

        if department_id:
            qs = qs.filter(enrollment__cohort__section__department_id=department_id)

        if term:
            qs = qs.filter(term=term)

        return qs

    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request):
        qs = self.filter_queryset(self.get_queryset())
        results = list(qs)

        total_credit = Decimal('0.0')
        total_weighted = Decimal('0.0')
        for result in results:
            if result.grade_point is None:
                continue
            total_credit += Decimal(result.subject.credit_hours)
            total_weighted += result.weighted_points

        gpa = None
        if total_credit > 0:
            gpa = (total_weighted / total_credit).quantize(Decimal('0.01'))

        serializer = self.get_serializer(results, many=True)
        return Response({
            'student_id': request.query_params.get('student_id') if not request.user.is_student() else request.user.id,
            'term': request.query_params.get('term'),
            'result_count': len(results),
            'total_credit_hours': int(total_credit),
            'total_weighted_points': float(total_weighted),
            'gpa': float(gpa) if gpa is not None else None,
            'results': serializer.data,
        })

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, (IsManagement | IsStudentReadOnly)]

    def get_queryset(self):
        user = self.request.user
        qs = Enrollment.objects.all()
        if user.is_authenticated:
            if user.is_student():
                return qs.filter(student=user)
        return qs

class StudentAttendanceViewSet(viewsets.ModelViewSet):
    queryset = StudentAttendance.objects.all()
    serializer_class = StudentAttendanceSerializer
    permission_classes = [IsAuthenticated, (IsManagement | IsStudentReadOnly)]

    def get_queryset(self):
        user = self.request.user
        qs = StudentAttendance.objects.all()
        if user.is_authenticated:
            if user.is_student():
                return qs.filter(enrollment__student=user)
        return qs

class TeacherAttendanceViewSet(viewsets.ModelViewSet):
    queryset = TeacherAttendance.objects.all()
    serializer_class = TeacherAttendanceSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrManagement]

    def get_queryset(self):
        user = self.request.user
        qs = TeacherAttendance.objects.all()
        if user.is_authenticated:
            if user.is_teacher():
                return qs.filter(teacher=user)
        return qs
