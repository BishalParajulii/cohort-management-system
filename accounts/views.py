from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, StudentProfile, TeacherProfile
from rest_framework.permissions import IsAuthenticated
from core.permissions import (
    IsAdmin, IsAdminOrCoordinator, IsManagement,
    IsStudentReadOnly, IsOwnerOrAdminOrCoordinator
)
from .serializers import (
    UserSerializer, StudentProfileSerializer, TeacherProfileSerializer, CustomTokenObtainPairSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsManagement]



class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdminOrCoordinator]

    def get_queryset(self):
        user = self.request.user
        qs = StudentProfile.objects.all()
        if user.is_authenticated:
            if user.is_student():
                return qs.filter(user=user)
        return qs



class TeacherProfileViewSet(viewsets.ModelViewSet):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdminOrCoordinator]

    def get_queryset(self):
        user = self.request.user
        qs = TeacherProfile.objects.all()
        if user.is_authenticated:
            if user.is_teacher():
                return qs.filter(user=user)
        return qs

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
