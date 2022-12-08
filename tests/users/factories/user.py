import factory
from factory.django import DjangoModelFactory

from tests import User


class UserFactory(DjangoModelFactory):
    """User model factory.

    https://factoryboy.readthedocs.io/en/stable/orms.html#django
    """

    email = factory.Faker("email")
    username = factory.LazyAttribute(lambda user: user.email)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    class Meta:
        model = User
        django_get_or_create = ["email"]
