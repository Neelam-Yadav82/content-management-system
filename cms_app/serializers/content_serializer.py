
from rest_framework import serializers
from cms_app.models import ContentItem
from common_utility.utils.date_time_util import get_date_time_dict_in_ist

class ContentItemSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True, max_length=30)
    body = serializers.CharField(required=True, max_length=300)
    summary = serializers.CharField(required=True, allow_blank=True)
    pdf_file = serializers.FileField(
        required=True, 
        allow_null=True,
        help_text="pdf file"
    )
    class Meta:
        model = ContentItem
        fields = [
            'id',
            'title',
            'body',
            'summary',
            'pdf_file',
            'categories',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['author', 'created_at', 'updated_at']
    def get_fields(self):
        """
        Customize fields based on the request method (POST or PUT).
        """
        fields = super().get_fields()
        request_method = (
            self.context["request"].method if "request" in self.context else None
        )
        if request_method == "POST":
            fields["title"].required = True
            fields["body"].required = True
            fields["summary"].required = True
            fields["pdf_file"].required = True
        elif request_method == "PUT":
            fields["title"].required = False
            fields["body"].required = False
            fields["summary"].required = False
            fields["pdf_file"].required = False

        return fields

    def validate_title(self, value):
        """
        Validate title.
        """
        if not isinstance(value, str):
            raise serializers.ValidationError("Invalid title. Must be a string.")
         
        # Check for title uniqueness
        if ContentItem.objects.filter(title=value).exists():
            # If it's an update, ensure the title is not being checked against itself
            if self.instance and self.instance.title == value:
                return value
            raise serializers.ValidationError("Title already exists. Please choose a different title.")

        return value

    def validate_body(self, value):
        """
        Validate body.
        """
        if not isinstance(value, str):
            raise serializers.ValidationError("Invalid body. Must be a string.")
        if len(value) > 300:
            raise serializers.ValidationError("Body length must not exceed 300 characters.")
        return value

    def validate_summary(self, value):
        """
        Validate summary.
        """
        if not isinstance(value, str):
            raise serializers.ValidationError("Invalid summary. Must be a string.")
        return value

    def create(self, validated_data):
        """
        Create a new content item instance.
        """
        validated_data['author'] = self.context['request'].user
        content_item = ContentItem.objects.create(**validated_data)
        return content_item

    def update(self, instance, validated_data):
        """
        Update an existing content item instance.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        """
        Convert model instance to representation.
        """
        representation = super().to_representation(instance)
        representation["created_at"] = get_date_time_dict_in_ist(
            datetime_utc_object=instance.created_at, noon_format=True
        )
        representation["updated_at"] = get_date_time_dict_in_ist(
            datetime_utc_object=instance.updated_at, noon_format=True
        )
        return representation
