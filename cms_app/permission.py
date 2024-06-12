from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
# Utils Imports
from common_utility.utils.constants import Role

class BaseAdminPermission(BasePermission):
    """
    Base permission class for checking if the requesting user is associated with an active admin profile.

    This permission class ensures that the requesting user has the necessary role and is linked to an active admin profile.
    If the user lacks the required permissions or is not associated with an active admin profile,
    a PermissionDenied exception is raised.

    Attributes:
        message (str): Default error message for permission denial.

    Raises:
        PermissionDenied: If the user lacks required permissions, is not linked to any admin profile,
            or their subscription is inactive.

    Returns:
        bool: True if the user has permission, False otherwise.
    """

    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        """
        Check if the requesting user has the necessary role and is associated with an active admin profile.

        Args:
            request: The HTTP request object.
            view: The view being accessed.

        Returns:
            bool: True if the user has the necessary permissions, False otherwise.
        """
        user = request.user

        if user.role.name == Role.SUPER_ADMIN and user.is_superuser and user.is_active:
            return True
        elif user.role.name == Role.AUTHER and user.is_active:
            return True
        return False


class AuthorAndAdminGetUpdateDeletePermissions(BaseAdminPermission):
    """
    Permission class to check if the requesting user has permission to access Content details.

    This class extends BaseAdminPermission to include object-level permissions.
    It allows superusers to have full access and authors to have access to their own content.

    Methods:
        has_object_permission: Checks if the user has permission to access a specific content object.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the requesting user has permission to access a specific content.

        Args:
            request: The HTTP request object.
            view: The view being accessed.
            obj: The content object being accessed.

        Returns:
            bool: True if the user has the necessary object-level permissions, False otherwise.

        Raises:
            PermissionDenied: If the user does not have permission to access the object.
        """
        user = request.user
        request_method = request.method

        if request_method in ["GET", "POST", "PUT", "DELETE"]:
            # Allow superuser to have object-level permission
            if user.is_superuser and user.is_active:
                return True
            # Allow the author to have object-level permission
            if obj.author == user:
                return True
            return False
        
        raise PermissionDenied("You do not have permission to access this resource.")
