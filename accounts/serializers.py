from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, StudentProfile, TeacherProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone', 'address']

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = '__all__'

class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = '__all__'

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Expose role directly in HTTP JSON response
        data['role'] = self.user.role
        data['username'] = self.user.username
        
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Inject role specifically into the encoded token string
        token['role'] = user.role
        token['username'] = user.username

        return token
