from django import forms

from users.models import User


class UserCreateForm(forms.ModelForm):
    """User creation form."""

    class Meta:
        model = User
        fields = ["username", "email", "password"]
