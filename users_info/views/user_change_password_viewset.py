import traceback
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class UserPasswordViewset(viewsets.ViewSet):
    """
    ViewSet for handling user password related operations.

    - get_authenticators: Method to determine authentication classes based on request method.
    - get_permissions: Method to determine permission classes based on action.
    - change_user_password: Method to change user's password.
    """

    def get_authenticators(self):
        """
        Method to determine authentication classes based on request method.
        """
        authentication_classes = []
        if self.request.method in ["GET", "POST"]:
            authentication_classes = [JWTAuthentication()]
        return authentication_classes

    def get_permissions(self):
        """
        Method to determine permission classes based on action.
        """
        permission_classes = []
        if self.action == "change_user_password":
            permission_classes = [IsAuthenticated()]
        return permission_classes

    def change_user_password(self, request):
        """
        Endpoint for changing user's password.

        Args:
            request: HTTP request object containing user authentication details and new password.

        Returns:
            Response: HTTP response object indicating the success or failure of the password change.

        This function handles the changing of a user's password. It expects an HTTP request object
        containing the user's current password and the new password.

        The function first checks if both the current password and the new password are provided. If
        not, it returns a 400 Bad Request response with an appropriate error message.

        It then checks if the new password is different from the current password. If not, it returns
        a 400 Bad Request response indicating that the new password cannot be the same as the current one.

        Next, it retrieves the user object from the request and validates the current password. If the
        current password is not correct, it returns a 400 Bad Request response.

        If all validations pass, it sets the new password for the user, saves the user object, and returns
        a 200 OK response indicating the successful password update.

        In case of any exceptions during the process, it catches them, logs the error, and returns a
        500 Internal Server Error response with the error message.
        """
        try:
            user = request.user

            if user.is_anonymous:
                return Response(
                    data={
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": "Token not provided.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            current_password = request.data.get("current_password", None)
            new_password = request.data.get("new_password", None)

            if not any([current_password, new_password]):
                return Response(
                    data={
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": "Missing field current_password or new_password",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if current_password == new_password:
                return Response(
                    data={
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": "New password can't be same as current password",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = request.user

            if not user.check_password(current_password):
                return Response(
                    data={
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": "Current password didn't match",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(new_password)
            user.save()

            return Response(
                data={
                    "status": status.HTTP_200_OK,
                    "message": "Password updated successfully",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print(e, traceback.format_exc())
            return Response(
                data={
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
