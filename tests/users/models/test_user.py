import pytest

from tests.testing_utils.testcases import ModelTestCase
from tests.users.factories import UserFactory


@pytest.mark.solo
class UserModelTest(ModelTestCase):
    """User model test."""

    def setUp(self) -> None:
        """Run this setup for each test."""
        self.first_name = "Test"
        self.last_name = "User"
        self.full_name = "Test User"
        assert self.full_name == f"{self.first_name} {self.last_name}"
        self.email = "user@example.com"
        self.user = UserFactory(
            first_name=self.first_name, last_name=self.last_name, email=self.email
        )


class UserModelGetterMethodsTest(UserModelTest):
    """User getter methods test case."""

    def setUp(self) -> None:
        """Run this set up before each test."""
        return super().setUp()

    def test_str_method(self) -> None:
        """__str__() method returns email field."""

        self.assertEqual(self.user.__str__(), self.full_name)
        self.assertEqual(str(self.user), self.full_name)

    def test_repr_method(self) -> None:
        """__repr__() method returns expected string."""

        expected = "User(id={}, name={}, email={})".format(
            self.user.id, self.full_name, self.email
        )

        self.assertEqual(self.user.__repr__(), expected)
        self.assertEqual(repr(self.user), expected)
