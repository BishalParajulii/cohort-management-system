from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, StudentProfile, TeacherProfile
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdmin , IsAdminOrCoordinator , IsHODOrAdmin , IsStudentReadOnly
from .serializers import (
    UserSerializer, StudentProfileSerializer, TeacherProfileSerializer, CustomTokenObtainPairSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated]

class TeacherProfileViewSet(viewsets.ModelViewSet):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer
    permission_classes = [IsAuthenticated , IsAdmin , IsAdminOrCoordinator]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
