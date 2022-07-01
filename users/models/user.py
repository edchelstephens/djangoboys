from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Our app user model."""

    def __repr__(self) -> str:
        """Python object string representation."""
        return "User(id={}, name={}, email={})".format(
            self.id, self.get_full_name(), self.email
        )
