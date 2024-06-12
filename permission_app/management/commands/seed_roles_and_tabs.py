from django.db import transaction
from django.core.management.base import BaseCommand
from permission_app.models import RoleMaster


class Command(BaseCommand):
    help = "Check and add missing roles and tabs in the database."

    def handle(self, *args, **options):
        # Define roles and permissions to add
        default_roles = [
            "SUPER_ADMIN_ROLE",
            "AUTHER_ROLE",
        ]

        # Check if roles and tabs are already present
        existing_roles = RoleMaster.objects.filter(name__in=default_roles).values_list(
            "name", flat=True
        )

        # Add roles and tabs if not present
        roles_to_add = list(set(default_roles) - set(existing_roles))

        # Add roles to the database
        roles_to_add_list = []

        # Add roles to the database
        if roles_to_add:
            # Add roles to the database within a transaction block for atomicity
            with transaction.atomic():
                for role_name in roles_to_add:
                    roles_to_add_list.append(RoleMaster(name=role_name))
                    self.stdout.write(self.style.SUCCESS(f"Roles to add: {role_name}"))

                # Bulk create roles
                RoleMaster.objects.bulk_create(roles_to_add_list)
                # Print success message
                self.stdout.write(
                    self.style.SUCCESS("=====================================\n")
                )
                for role in roles_to_add_list:
                    self.stdout.write(
                        self.style.SUCCESS(f"Role added: {role} successfully.")
                    )
                self.stdout.write(
                    self.style.SUCCESS("=====================================\n")
                )
        # Print success message if no roles need to be added
        elif not roles_to_add:
            self.stdout.write(self.style.SUCCESS("All roles are already present."))
