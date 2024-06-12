from django.urls import path,include

from cms_app.views.content_viewset import ContentItemViewset

urlpatterns = [
    path(
        "content/",
        include(
            [
                path(
                    "<int:content_id>/",
                    ContentItemViewset.as_view(
                        {
                            "get": "get_content_details",
                        }
                    ),
                ),
                path(
                    "all/",
                    ContentItemViewset.as_view(
                        {
                            "get": "get_all_content_details",
                        }
                    ),
                ),
                path(
                    "add/",
                    ContentItemViewset.as_view(
                        {
                            "post": "add_content_details",
                        }
                    ),
                ),
                path(
                    "update/<int:content_id>/",
                    ContentItemViewset.as_view(
                        {
                            "put": "update_content_details",
                        }
                    ),
                ),
                path(
                    "delete/<int:content_id>/",
                    ContentItemViewset.as_view(
                        {
                            "get": "delete_content_details",
                        }
                    ),
                ),
            ]
        ),
    ),
]
