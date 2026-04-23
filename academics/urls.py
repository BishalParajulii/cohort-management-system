from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SubjectViewSet, EnrollmentViewSet,
    StudentAttendanceViewSet, TeacherAttendanceViewSet
)

router = DefaultRouter()
router.register(r'subjects', SubjectViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'student-attendances', StudentAttendanceViewSet)
router.register(r'teacher-attendances', TeacherAttendanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
