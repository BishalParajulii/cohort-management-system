from rest_framework import permissions
from institutions.models import Department

class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_admin())


class IsAdminOrCoordinator(permissions.BasePermission):

    def has_permission(self,request , view):
        return bool(request.user and request,user.is_authenticated and (request.user.is_admin or request.user.is_coordinator))


class IsHODOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if not bool(request.user and request.user.is_authenticated):
            return False
            
        if request.user.is_admin():
            return True
            
        is_hod = Department.objects.filter(head=request.user).exists()
        return is_hod

class IsStudentReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if not bool(request.user and request.user.is_authenticated):
            return False
            
        if request.user.is_student():
            return request.method in permissions.SAFE_METHODS
            
        return True
