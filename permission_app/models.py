from django.db import models

class RoleMaster(models.Model):
    """
    Model to store role details.
    """

    name = models.CharField(max_length=100, help_text="Enter the name of the role.")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "role_master"
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        ordering = ["-id"]
