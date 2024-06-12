import traceback
from django.contrib.auth.models import AnonymousUser
from rest_framework import status, viewsets,status, exceptions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from cms_app.serializers.content_serializer import ContentItemSerializer
from users_info.serializers.user_serializers import UserSerializer
from cms_app.permission import (
    BaseAdminPermission,
    AuthorAndAdminGetUpdateDeletePermissions,
)
from common_utility.utils.serializers_errors import serializer_error
from common_utility.utils.pagination_utility import pagination_utility
from cms_app.models import ContentItem
from users_info.models import UserDetails

class ContentItemViewset(viewsets.ViewSet):
    """
    ViewSet for handling ContentItem operations including retrieving, adding, updating, and deleting content items.
    """
    def get_authenticators(self):
        """
        Override to return the authentication classes based on the request method.
        """
        authentication_classes = []
        if self.request.method in ["GET", "DELETE", "POST", "PUT"]:
            authentication_classes = [JWTAuthentication()]
        return authentication_classes

    def get_permissions(self):
        """
        Override to return the permission classes based on the action.
        """
        permission_classes = []
        if self.action in ["add_content_details"]:
            permission_classes += [IsAuthenticated(), BaseAdminPermission()]
        elif self.action in ["get_content_details", "get_all_content_details", "update_content_details","delete_content_details"]:
            permission_classes += [
                IsAuthenticated(),
                AuthorAndAdminGetUpdateDeletePermissions(),
            ]
        return permission_classes

    def get_content_details(self, request, content_id):
        """
        Retrieve the details of a specific content item.

        Args:
            request: The HTTP request object.
            content_id: The ID of the content item to retrieve.

        Returns:
            Response: The HTTP response with content item details or an error message.
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
                content_obj = ContentItem.objects.get(
                    id=content_id
                )
            except content_obj.DoesNotExist:
                return Response(
                    data={
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": "No content message with given content id.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                self.check_object_permissions(request, content_obj)
            except exceptions.PermissionDenied:
                return Response(
                    data={
                        "status": status.HTTP_403_FORBIDDEN,
                        "error": "You do not have permission to access this content.",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            serializer = ContentItemSerializer(
                instance=content_obj
            )

            if serializer.data:
                return Response(
                    data={
                        "status": status.HTTP_200_OK,
                        "success": serializer.data,
                        "message": "content details reterived.",
                    },
                    status=status.HTTP_200_OK,
                )
            else:
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

    def get_all_content_details(self, request):
        """
        Retrieve details of all content items created by the authenticated user.

        Args:
            request: The HTTP request object.

        Returns:
            Response: The HTTP response with a list of content items or an error message.
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
                page = int(request.query_params.get("page", 1))
                items = int(request.query_params.get("items", 10))
            except Exception as e:
                page, items = 1, 10

            page = 1 if page == 0 else page
            items = 10 if 0 < items <= 1 else items

            offset = (page - 1) * items
            limit = page * items
            user = UserDetails.objects.get(id=user.id)
            content_obj = ContentItem.objects.filter(
                author=user
            )
            if not content_obj.exists():
                return Response(
                    data={
                        "status": status.HTTP_200_OK,
                        "success": [],
                        "message": "Auther currently have no content.",
                    },
                    status=status.HTTP_200_OK,
                )

            if not content_obj[offset:limit]:
                return Response(
                    data={
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": "Invalid page number",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = ContentItemSerializer(
                instance=content_obj[offset:limit], many=True
            )

            if serializer.data:
                paginated_data = pagination_utility(
                    total_entries=content_obj,
                    page=page,
                    items=items,
                )
                data_to_send = {
                    "user": UserSerializer(instance=user).data,
                    "book_content_details": serializer.data,
                }
                return Response(
                    data={
                        "status": status.HTTP_200_OK,
                        "success": data_to_send,
                        "page_details": paginated_data,
                        "message": "contents details reterived.",
                    },
                    status=status.HTTP_200_OK,
                )
            else:
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

    def add_content_details(self, request):
        """
        Add a new content item.

        Args:
            request: The HTTP request object containing content item data.

        Returns:
            Response: The HTTP response with the added content item details or an error message.
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

            serializer = ContentItemSerializer(
                data=request.data, context={"request": request}
            )

            if serializer.is_valid():
                serializer.save()  # Save the instance first
                return Response(
                    data={
                        "status": status.HTTP_201_CREATED,
                        "success": serializer.data,
                        "message": "content details added.",
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
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

    def update_content_details(self, request,content_id):
        """
        Update the details of a specific content item.

        Args:
            request: The HTTP request object containing updated content item data.
            content_id: The ID of the content item to update.

        Returns:
            Response: The HTTP response with the updated content item details or an error message.
        """
        try:
            user = request.user

            if isinstance(user, AnonymousUser):
                return Response(
                    data={
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": "Token not provided.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not content_id:
                return Response(
                    data={
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": "content ID is mandatory.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                content_obj = ContentItem.objects.get(
                    id=content_id
                )
            except ContentItem.DoesNotExist:
                return Response(
                    data={
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": "No content with given content id.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                self.check_object_permissions(request, content_obj)
            except exceptions.PermissionDenied:
                return Response(
                    data={
                        "status": status.HTTP_403_FORBIDDEN,
                        "error": "You do not have permission to access this content.",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            serializer = ContentItemSerializer(
                data=request.data,
                instance=content_obj,
                partial=True,
                context={"request": request},
            )

            if serializer.is_valid():
                serializer.save()  # Save the instance
                return Response(
                    data={
                        "status": status.HTTP_200_OK,
                        "success": serializer.data,
                        "message": "content details updated",
                    },
                    status=status.HTTP_200_OK,
                )
            elif serializer.errors:
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

    def delete_content_details(self, request,content_id):
        """
        Delete a specific content item.

        Args:
            request: The HTTP request object.
            content_id: The ID of the content item to delete.

        Returns:
            Response: The HTTP response indicating the success or failure of the deletion operation.
        """
        try:
            user = request.user

            if isinstance(user, AnonymousUser):
                return Response(
                    data={
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": "Token not provided.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not content_id:
                return Response(
                    data={
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": "content ID is mandatory.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                content_obj = ContentItem.objects.get(
                    id=content_id
                )
            except ContentItem.DoesNotExist:
                return Response(
                    data={
                        "status": status.HTTP_400_BAD_REQUEST,
                        "error": "No content with given content id.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                self.check_object_permissions(request, content_obj)
            except exceptions.PermissionDenied:
                return Response(
                    data={
                        "status": status.HTTP_403_FORBIDDEN,
                        "error": "You do not have permission to delete this content.",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Perform the delete operation
            content_obj.delete()

            return Response(
                data={
                    "status": status.HTTP_200_OK,
                    "success": [],
                    "message": "content deleted successfully.",
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

