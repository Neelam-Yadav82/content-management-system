from django.db import models
from users_info.models import UserDetails

class ContentItem(models.Model):
    author = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    body = models.TextField(max_length=300)
    summary = models.TextField(blank=True, null=True)
    pdf_file = models.FileField(
        upload_to="content_management_pdf",
        null=True,
        blank=True,
        verbose_name="Content Pdf file",
        help_text="pdf file",
    )
    categories = models.CharField(max_length=255, blank=True, null=True)
    
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(auto_now=True)
    REQUIRED_FIELDS = [
        "title",
        "body",
        "summary",
        "pdf_file",
    ]
    class Meta:
        db_table = "content_item_table"
        ordering = ["-created_at"]
        verbose_name_plural = "Content Details"
        verbose_name = "Content Detail"
