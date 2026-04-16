from rest_framework import permissions
from institutions.models import Department

class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_admin())


class IsAdminOrCoordinator(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            (request.user.is_admin() or request.user.is_coordinator())
        )


class IsTeacher(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_teacher())


class IsCoordinator(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_coordinator())


class IsHOD(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_hod())


class IsManagement(permissions.BasePermission):

    def has_permission(self, request, view):
        if not bool(request.user and request.user.is_authenticated):
            return False
        
        return (
            request.user.is_admin() or 
            request.user.is_coordinator() or
            request.user.is_hod()
        )




class IsTeacherOrManagement(permissions.BasePermission):

    def has_permission(self, request, view):
        if not bool(request.user and request.user.is_authenticated):
            return False

        return (
            request.user.is_teacher() or
            request.user.is_admin() or
            request.user.is_coordinator() or
            request.user.is_hod()
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsOwnerOrAdminOrCoordinator(permissions.BasePermission):


    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if user.is_admin() or user.is_coordinator() or user.is_hod():
            return True

        if hasattr(obj, 'user'):
            return obj.user == user

        if hasattr(obj, 'student'):
            return obj.student == user

        if hasattr(obj, 'teacher'):
            return obj.teacher == user

        return obj == user


class IsStudentReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if not bool(request.user and request.user.is_authenticated):
            return False
            
        if request.user.is_student():
            return request.method in permissions.SAFE_METHODS
            
        return True
