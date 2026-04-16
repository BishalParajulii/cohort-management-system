from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Subject, Enrollment, StudentAttendance, TeacherAttendance
from .serializers import (
    SubjectSerializer, EnrollmentSerializer,
    StudentAttendanceSerializer, TeacherAttendanceSerializer
)
from core.permissions import *

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated, (IsManagement | IsStudentReadOnly)]

    def get_queryset(self):
        user = self.request.user
        qs = Subject.objects.all()
        if user.is_authenticated and user.is_hod():
            qs = qs.filter(department__head=user)
        return qs

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
            if user.is_hod():
                return qs.filter(cohort__section__department__head=user)
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
            if user.is_hod():
                return qs.filter(enrollment__cohort__section__department__head=user)
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
            if user.is_hod():
                return qs.filter(teacher__teacher_profile__department__head=user)
        return qs
