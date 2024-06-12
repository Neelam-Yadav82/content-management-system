import traceback
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from users_info.models import UserDetails
from users_info.serializers.user_login_serializer import UserLoginSeriaizer
from users_info.serializers.user_serializers import UserSerializer
from common_utility.utils.serializers_errors import serializer_error


class UserLoginViewset(viewsets.ViewSet):
    """
    ViewSet for handling user login and user details retrieval.

    - get_authenticators: Method to determine authentication classes based on request method.
    - get_permissions: Method to determine permission classes based on action.
    - login_user: Method to authenticate and login user.
    - get_user_details: Method to fetch user details.
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
        if self.action == "login_user":
            permission_classes = [AllowAny()]
        elif self.action == "get_user_details":
            permission_classes = [IsAuthenticated()]
        return permission_classes

    def login_user(self, request):
        """
        Endpoint for authenticating and logging in a user.

        Args:
            request: HTTP request object containing user login data.

        Returns:
            Response: HTTP response object indicating the success or failure of the login attempt.

        This function handles the authentication and login of a user. It expects an HTTP request object
        containing user login data, including email and password.

        The function first validates the input data using a serializer. If the data is valid, it attempts
        to retrieve the user object based on the provided email. If the user is found and not deleted, it
        generates access and refresh tokens for the user using the RefreshToken module.

        If the user account is deleted, it returns a 200 OK response with an appropriate error message.

        If any validation fails or exceptions occur during the process, it returns a 400 Bad Request or
        500 Internal Server Error response with the error message.
        """
        try:
            serializer = UserLoginSeriaizer(data=request.data)
            if serializer.is_valid():
                user = UserDetails.objects.get(email=serializer.validated_data["email"])
                if not user:
                    return Response(
                        data={
                            "status": status.HTTP_200_OK,
                            "error": "User account Does Not Exists",
                        },
                        status=status.HTTP_200_OK,
                    )
                user_token = RefreshToken.for_user(user)
                token_data = {
                    "access": str(user_token.access_token),
                    "refresh": str(user_token),
                }
                return Response(
                    data={
                        "status": status.HTTP_200_OK,
                        "message": "Login successfully",
                        "success": token_data,
                    },
                    status=status.HTTP_200_OK,
                )
            elif not serializer.is_valid():
                serializer_errors = serializer.errors
                error_message = serializer_error(serializer_errors)
                return Response(
                    data={
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": error_message,
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

    def get_user_details(self, request):
        """
        Endpoint for fetching user details.

        Args:
            request: HTTP request object containing user authentication details.

        Returns:
            Response: HTTP response object containing user details or error message.

        This function handles the fetching of user details. It expects an HTTP request object
        containing user authentication details.

        The function first retrieves the user object from the request. If the user account is
        deleted, it returns a 200 OK response with an appropriate error message.

        If the user object is found, it serializes the user details and constructs a response
        containing the user details. If serialization fails, it returns a 400 Bad Request response
        with the serializer errors.

        In case of any exceptions during the process, it catches them, logs the error, and returns
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

            serializer = UserSerializer(user)
            if serializer.data:
                return Response(
                    data={
                        "status": status.HTTP_200_OK,
                        "message": "User details fetched successfully",
                        "success": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            elif serializer.errors:
                return Response(
                    data={
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": serializer.errors,
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
