from rest_framework.permissions import BasePermission

class IsOwnerOrStaff(BasePermission):
    """
    Access is only allowed if the user is the owner or is a staff member.
    This includes checking for authentication.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user and request.user.is_staff:
            return True
        return obj.user == request.user