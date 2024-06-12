import re

# Django imports
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users_info.models import UserDetails
from permission_app.models import RoleMaster
from permission_app.serializers.role_serializer import RolemasterSerializer
from common_utility.utils.constants import Role
from common_utility.utils.date_time_util import get_date_time_dict_in_ist


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration functionality.
    """

    full_name = serializers.CharField(required=True)  # CharField for user's full name
    
    email = serializers.EmailField(  # EmailField for user's email address
        required=True,
    )
    phone = serializers.CharField(  # CharField for user's mobile number
        required=True,
    )
    pincode = serializers.IntegerField(required=True)
    password = serializers.CharField(  # CharField for user's password
        write_only=True,
        required=True,
    )
    confirm_password = serializers.CharField(
        write_only=True, required=True
    )  # CharField for confirming user's password
    role = serializers.CharField(
        write_only=True, required=False
    )  # CharField for user's role (optional)

    class Meta:
        model = UserDetails
        fields = [
            "full_name",
            "email",
            "phone",
            "address",
            "city",
            "state",
            "country",
            "pincode",
            "password",
            "confirm_password",
            "role",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "full_name": {"required": True},
            "email": {"required": True},
            "phone": {"required": True},
            "pincode": {"required": True},
        }

    def get_fields(self):
        """
        Customize fields based on the request method (POST or PUT).
        """
        fields = super().get_fields()
        request_method = (
            self.context["request"].method if "request" in self.context else None
        )
        if request_method == "POST":
            fields["password"].required = True
            fields["confirm_password"].required = True
        elif request_method == "PUT":
            fields["password"].required = False
            fields["confirm_password"].required = False

        return fields
    
    def validate_full_name(self, value):
        if not value:
            raise serializers.ValidationError("Full Name is required.")
        return value

    def validate_email(self, value):
        try:
            validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError("Invalid email format.")

        if UserDetails.objects.filter(email=value).exists():
            raise serializers.ValidationError(f"Email '{value}' already exists.")
        return value

    def validate_phone(self, value):
        if UserDetails.objects.filter(phone=value).exists():
            raise serializers.ValidationError(
                f"Mobile number '{value}' already exists."
            )
        return value

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("Password is required.")

        if len(value) < 8:
            raise serializers.ValidationError(
                f"Password must be at least 8 characters long."
            )

        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError(
                f"Password must contain at least one uppercase letter."
            )

        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError(
                f"Password must contain at least one lowercase letter."
            )

        if not re.search(r"\d", value):
            raise serializers.ValidationError(
                f"Password must contain at least one digit."
            )

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise serializers.ValidationError(
                f"Password must contain at least one special character."
            )

        return make_password(value)

    def validate_confirm_password(self, value):
        if not value:
            raise serializers.ValidationError("Confirm Password is required.")

        password = self.initial_data.get("password")

        if not password:
            raise serializers.ValidationError("Enter Password.")

        if password != value:
            raise serializers.ValidationError(
                f"Confirm Passwords and Password didn't match."
            )

        return value
    
    def validate_pincode(self, value):
        if not value:
            raise serializers.ValidationError("pincode is required.")
        return value

    def create(self, validated_data):
        """
        Method to create a new user instance.

        - validated_data: Dictionary containing validated user data.
        """
        role = validated_data.pop("role", None)

        # Check if role is present in validated data else set role as GUEST
        validated_data["role_id"] = (
            RoleMaster.objects.get(name=role).id
            if role
            else RoleMaster.objects.get(name=Role.AUTHER).id
        )
        # Remove password and confirm_password from validated data
        confirm_password = validated_data.pop("confirm_password", None)
        validated_data.pop("password", None)
        validated_data["is_auther"]=True

        # Create user instance
        user = UserDetails.objects.create(**validated_data)

        return user

    def to_representation(self, instance):
        """
        Method to convert model instance to representation.

        - instance: UserDetails instance to convert.
        """
        representation = super().to_representation(instance)

        representation["role"] = RolemasterSerializer(instance.role).data
        representation["created_at"] = get_date_time_dict_in_ist(
            datetime_utc_object=instance.created_at, noon_format=True
        )
        representation["updated_at"] = get_date_time_dict_in_ist(
            datetime_utc_object=instance.updated_at, noon_format=True
        )
        return representation
