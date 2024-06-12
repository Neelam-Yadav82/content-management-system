import traceback
from django.contrib.auth.hashers import make_password
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from users_info.serializers.user_registration_serializer import (
    UserRegistrationSerializer,
)
from users_info.models import UserDetails
from common_utility.utils.serializers_errors import serializer_error


class UserRegistrationViewset(viewsets.ViewSet):
    """
    ViewSet for user registration and email/mobile number verification.

    - register_user: Method to register a new user.
    - verify_if_email_already_exists: Method to check if the provided email already exists.
    - verify_if_mobile_number_already_exists: Method to check if the provided mobile number already exists.
    """

    authentication_classes = []
    permission_classes = (AllowAny,)

    def register_user(self, request):
        """
        Endpoint for registering a new user.

        Args:
            request: HTTP request object containing user registration data.

        Returns:
            Response: HTTP response object indicating the success or failure of the user registration attempt.

        This method registers a new user based on the provided user registration data. It expects an HTTP request
        object containing the user registration details.

        The function first retrieves the confirm password from the request data. It then initializes a UserRegistrationSerializer
        instance with the provided data.

        If the serializer is not valid, it extracts and formats the serializer errors, returning a 400 Bad Request response
        with the error details.

        If the serializer is valid, it saves the user object and sets the password using the confirm password. It then returns
        a 201 Created response with a success message and the serialized user data.

        If any exceptions occur during the process, it catches them, logs the error, and returns a 500 Internal Server Error
        response with the error message.
        """
        try:
            confirm_password = request.data.get("confirm_password", None)
            serializer = UserRegistrationSerializer(data=request.data)

            if not serializer.is_valid():
                serializer_errors = serializer.errors
                error_message = serializer_error(serializer_errors)
                return Response(
                    data={
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": error_message,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            else:
                user = serializer.save()
                user.set_password(confirm_password)
                user.save()
                return Response(
                    {
                        "status": status.HTTP_201_CREATED,
                        "message": "User registration done",
                        "success": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
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

    def verify_if_email_already_exists(self, request):
        """
        Endpoint for checking if the provided email already exists.

        Args:
            request: HTTP request object containing the email to be checked.

        Returns:
            Response: HTTP response object indicating the success or failure of the email existence check.

        This method checks if the provided email already exists in the database. It expects an HTTP request object
        containing the email to be checked.

        The function retrieves the email from the request data. If the email is not provided, it returns a 400 Bad Request
        response with an appropriate error message.

        It then queries the database to check if the email exists. If the email exists, it returns a 400 Bad Request response
        with an error message indicating that the email already exists. If the email is unique, it returns a 200 OK response
        with a message indicating that the email is unique.

        If any exceptions occur during the process, it catches them, logs the error, and returns a 500 Internal Server Error
        response with the error message.
        """

        try:
            email = request.data.get("email", None)

            if not email:
                return Response(
                    data={
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": "email not provided",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            is_email = UserDetails.objects.filter(email=email).only("email")

            status_code = (
                status.HTTP_200_OK
                if not is_email.exists()
                else status.HTTP_400_BAD_REQUEST
            )
            key_word = "message" if not is_email.exists() else "error"

            key_word_value = (
                "Email is unique" if not is_email.exists() else "Email already exists"
            )

            return Response(
                data={
                    "status": status_code,
                    key_word: key_word_value,
                },
                status=status_code,
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

    def verify_if_mobile_number_already_exists(self, request):
        """
        Endpoint for checking if the provided mobile number already exists.

        Args:
            request: HTTP request object containing the mobile number to be checked.

        Returns:
            Response: HTTP response object indicating the success or failure of the mobile number existence check.

        This method checks if the provided mobile number already exists in the database. It expects an HTTP request object
        containing the mobile number to be checked.

        The function retrieves the mobile number from the request data. If the mobile number is not provided, it returns
        a 400 Bad Request response with an appropriate error message.

        It then queries the database to check if the mobile number exists. If the mobile number exists, it returns a
        400 Bad Request response with an error message indicating that the mobile number already exists. If the mobile number
        is unique, it returns a 200 OK response with a message indicating that the mobile number is unique.

        If any exceptions occur during the process, it catches them, logs the error, and returns a 500 Internal Server Error
        response with the error message.
        """

        try:
            phone = request.data.get("phone", None)

            if not phone:
                return Response(
                    data={
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": "Mobile number not provided",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            is_mobile_number_present = UserDetails.objects.filter(
                phone=phone
            ).only("phone")

            status_code = (
                status.HTTP_200_OK
                if not is_mobile_number_present.exists()
                else status.HTTP_400_BAD_REQUEST
            )
            key_word = "message" if not is_mobile_number_present.exists() else "error"

            key_word_value = (
                "Mobile_number is unique"
                if not is_mobile_number_present.exists()
                else "Mobile_number already exists"
            )

            return Response(
                data={
                    "status": status_code,
                    key_word: key_word_value,
                },
                status=status_code,
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
