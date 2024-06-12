from django.contrib.auth.base_user import BaseUserManager
from permission_app.models import RoleMaster
from common_utility.utils.constants import Role


class CustomManager(BaseUserManager):
    def _create_user(
        self,
        full_name: str,
        email: str,
        password: str,
        phone: str,
        **kwargs,
    ):
        if not email:
            return ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(
            full_name=full_name,
            email=email,
            phone=phone,
            **kwargs,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email: str, password: str, phone: str, **kwargs):
        kwargs.setdefault("is_active", True)
        kwargs.setdefault("is_auther", True)
        try:
            auther_role = RoleMaster.objects.get(name=Role.AUTHER)
        except RoleMaster.DoesNotExist:
            raise ValueError(f"Role {Role.AUTHER} does not exist in the database")

        kwargs.setdefault("role_id", auther_role.id)

        return self._create_user(
            email=email, password=password, phone=phone, **kwargs
        )

    def create_superuser(self, email: str, password: str, phone: str, **kwargs):
        try:
            super_admin_role = RoleMaster.objects.get(name=Role.SUPER_ADMIN)
        except RoleMaster.DoesNotExist:
            raise ValueError(f"Role {Role.SUPER_ADMIN} does not exist in the database")
        kwargs.setdefault("is_active", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("role_id", super_admin_role.id)

        return self._create_user(
            email=email, password=password, phone=phone, **kwargs
        )
