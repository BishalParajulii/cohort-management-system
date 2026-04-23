from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Institution, Department, AcademicYear, Grade, Shift, Section, Cohort
from .serializers import (
    InstitutionSerializer, DepartmentSerializer, AcademicYearSerializer,
    GradeSerializer, ShiftSerializer, SectionSerializer, CohortSerializer
)
from core.permissions import IsAdmin, IsManagement

class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsManagement]

    def get_queryset(self):
        user = self.request.user
        qs = Department.objects.all()
        return qs

class AcademicYearViewSet(viewsets.ModelViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class ShiftViewSet(viewsets.ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated, IsManagement]

    def get_queryset(self):
        user = self.request.user
        qs = Section.objects.all()
        return qs

class CohortViewSet(viewsets.ModelViewSet):
    queryset = Cohort.objects.all()
    serializer_class = CohortSerializer
    permission_classes = [IsAuthenticated, IsManagement]

    def get_queryset(self):
        user = self.request.user
        qs = Cohort.objects.all()
        return qs
