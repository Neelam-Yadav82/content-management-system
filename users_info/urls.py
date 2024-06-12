from django.urls import path, include
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView
from users_info.views import (
    user_registration_viewset,
    user_login_viewset,
    user_logout_viewset,
    user_change_password_viewset,
)

urlpatterns = [
    path(
        "registration/",
        include(
            [
                path(
                    "",
                    user_registration_viewset.UserRegistrationViewset.as_view(
                        {
                            "post": "register_user",
                        }
                    ),
                ),
                path(
                    "verify-email/",
                    user_registration_viewset.UserRegistrationViewset.as_view(
                        {
                            "post": "verify_if_email_already_exists",
                        }
                    ),
                ),
                path(
                    "verify-mobile-number/",
                    user_registration_viewset.UserRegistrationViewset.as_view(
                        {
                            "post": "verify_if_mobile_number_already_exists",
                        }
                    ),
                ),
            ]
        ),
    ),
    path(
        "authenticate/",
        user_login_viewset.UserLoginViewset.as_view(
            {
                "get": "get_user_details",
                "post": "login_user",
            }
        ),
    ),
    path(
        "authenticate/logout/",
        user_logout_viewset.UserLogoutViewset.as_view(
            {
                "get": "logout_user",
            }
        ),
    ),
    path(
        "authenticate/change-password/",
        user_change_password_viewset.UserPasswordViewset.as_view(
            {
                "post": "change_user_password",
            }
        ),
    ),
   
]
