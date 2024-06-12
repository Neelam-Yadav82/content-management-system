from rest_framework import serializers
from users_info.models import UserDetails
from common_utility.utils.date_time_util import get_date_time_dict_in_ist
from permission_app.serializers.role_serializer import RolemasterSerializer


class UserMinimalDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for minimal user details.

    - role: RolemasterSerializer for user role details.
    """

    role = RolemasterSerializer()  # RolemasterSerializer for user role details

    class Meta:
        model = UserDetails
        fields = [
            "id",
            "full_name",
            "email",
            "phone",
            "is_active",
            "role",
        ]


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed user information.

    - to_representation: Method to convert model instance to representation.
    """

    class Meta:
        model = UserDetails
        fields = [
            "id",
            "full_name",
            "email",
            "phone",
            "address",
            "city",
            "state",
            "country",
            "pincode",
            "is_active",
            "is_auther",
            "is_superuser",
            "role",
            "created_at",
            "updated_at",
        ]

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
