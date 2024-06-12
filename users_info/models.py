from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.base_user import AbstractBaseUser
from simple_history.models import HistoricalRecords

# from permission_app.models.role_master_model import RoleMaster
from permission_app.models import RoleMaster
from users_info.managers import CustomManager

class UserDetails(AbstractBaseUser):
    role = models.ForeignKey(
        RoleMaster,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="user_role",
    )
    email = models.EmailField(unique=True, db_index=True, null=True, blank=True)
    full_name = models.CharField(max_length=50, db_index=True, null=True, blank=True)
    phone = models.CharField(max_length=10, db_index=True, blank=True, null=True)
    address = models.TextField(blank=True, db_index=True, null=True)
    city = models.CharField(max_length=255, db_index=True, blank=True, null=True)
    state = models.CharField(max_length=255, db_index=True, blank=True, null=True)
    country = models.CharField(max_length=255, db_index=True, blank=True, null=True)
    pincode = models.CharField(max_length=6, db_index=True, null=True, blank=True)

    is_auther = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff=models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    objects = CustomManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "full_name",
        "phone",
    ]
    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app `app_label`?
        """
        # Simplest possible answer: Yes, always
        return True

    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?
        """
        return True

    def __str__(self):
          return  self.full_name
         
    class Meta:
        db_table = "user_details_table"
        ordering = ["-created_at"]
        verbose_name_plural = "User Details"
        verbose_name = "User Detail"
