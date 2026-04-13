from rest_framework import viewsets
from .models import Institution, Department, AcademicYear, Grade, Shift, Section, Cohort
from .serializers import (
    InstitutionSerializer, DepartmentSerializer, AcademicYearSerializer,
    GradeSerializer, ShiftSerializer, SectionSerializer, CohortSerializer
)

class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer



class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Department.objects.all()
        if user.is_authenticated and not user.is_admin():
            qs = qs.filter(head=user)
        return qs

class AcademicYearViewSet(viewsets.ModelViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

class ShiftViewSet(viewsets.ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Section.objects.all()
        if user.is_authenticated and not user.is_admin():
            qs = qs.filter(department__head=user)
        return qs

class CohortViewSet(viewsets.ModelViewSet):
    queryset = Cohort.objects.all()
    serializer_class = CohortSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Cohort.objects.all()
        if user.is_authenticated and not user.is_admin():
            qs = qs.filter(section__department__head=user)
        return qs
