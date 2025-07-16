from rest_framework.permissions import BasePermission

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "Student"
    
class IsFranchise(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "franchise"

class IsCounselor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "counselor"

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        
        # return request.user.is_authenticated and request.user.role == "admin"
        return request.user.is_authenticated and request.user.role == "Admin"
