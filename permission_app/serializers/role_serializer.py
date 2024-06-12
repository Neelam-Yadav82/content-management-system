from rest_framework import serializers
from permission_app.models import RoleMaster


class RolemasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleMaster
        fields = [
            "id",
            "name",
        ]
