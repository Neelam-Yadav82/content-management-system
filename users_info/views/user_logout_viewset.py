import traceback
from django.contrib.auth import logout
from django.contrib.auth.models import AnonymousUser
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import OutstandingToken


class UserLogoutViewset(viewsets.ViewSet):
    """
    ViewSet for handling user logout.

    - get_authenticators: Method to determine authentication classes based on request method.
    - get_permissions: Method to determine permission classes based on action.
    - logout_user: Method to logout the authenticated user.
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
        if self.action == "logout_user":
            permission_classes = [IsAuthenticated()]
        return permission_classes

    def logout_user(self, request):
        """
        Endpoint for logging out the authenticated user.

        Args:
            request: HTTP request object containing user authentication details.

        Returns:
            Response: HTTP response object indicating the success or failure of the logout attempt.

        This function handles the logout of the authenticated user. It expects an HTTP request object
        containing user authentication details.

        The function first retrieves the user object from the request. If the user account is deleted,
        it returns a 200 OK response with an appropriate error message.

        It then retrieves the outstanding refresh tokens associated with the user. If no outstanding
        tokens are found, it returns a 400 Bad Request response with an error message.

        For each outstanding token, it attempts to blacklist the token using the RefreshToken module.
        If any token is invalid, it continues to the next token.

        After blacklisting all outstanding tokens, it logs out the user using the `logout` function.

        If any exceptions occur during the process, it catches them, logs the error, and returns
        a 500 Internal Server Error response with the error message.
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

            try:
                outstanding_tokens = OutstandingToken.objects.filter(user=user)

                if not outstanding_tokens:
                    return Response(
                        data={
                            "status": status.HTTP_400_BAD_REQUEST,
                            "error": "Refresh token not found.",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                for token in outstanding_tokens:
                    try:
                        refresh_token = RefreshToken(token.token)
                        refresh_token.blacklist()
                    except TokenError as e:
                        print(str(e))
                        continue

                logout(request)
                return Response(
                    {
                        "status": status.HTTP_200_OK,
                        "message": "Logout successful.",
                    },
                    status=status.HTTP_200_OK,
                )
            except TokenError:
                return Response(
                    data={
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": "Invalid refresh token.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
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
