from rest_framework import serializers

from users_info.models import UserDetails


class UserLoginSeriaizer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = UserDetails
        fields = [
            "email",
            "password",
        ]

    def validate(self, attrs):
        """
        Method to validate user credentials.

        - attrs: Dictionary containing the validated data.
        """
        try:
            user = UserDetails.objects.only("email").get(email=attrs["email"])

        except UserDetails.DoesNotExist:
            raise serializers.ValidationError(f"Incorrect Email:{attrs.get('email')}")
        except UserDetails.MultipleObjectsReturned:
            raise serializers.ValidationError("Multiple entries found")

        if not user.check_password(attrs["password"]):
            raise serializers.ValidationError(f"Incorrect password")
        return attrs
