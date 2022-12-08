from django.contrib.auth.models import Permission

from tests import User


class PermissionRequiredTestMixin:
    """Mixin for tests with permission requirements."""

    def add_permission(self, user: User, codename: str, use_latest=False) -> None:
        """Add permission on user."""

        permissions = Permission.objects.filter(codename=codename)
        if use_latest:
            permission = permissions.last()
        else:
            permission = permissions.first()

        user.user_permissions.add(permission)

    def add_view_permission(self, user: User, codename: str, use_latest=False) -> None:
        """An alias for add_permission() for testing views with PermissionRequiredMixin."""
        self.add_permission(user, codename, use_latest)
