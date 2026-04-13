from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    InstitutionViewSet, DepartmentViewSet, AcademicYearViewSet,
    GradeViewSet, ShiftViewSet, SectionViewSet, CohortViewSet
)

router = DefaultRouter()
router.register(r'institutions', InstitutionViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'academic-years', AcademicYearViewSet)
router.register(r'grades', GradeViewSet)
router.register(r'shifts', ShiftViewSet)
router.register(r'sections', SectionViewSet)
router.register(r'cohorts', CohortViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
