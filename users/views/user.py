from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views import View

from users.forms.user import UserCreateForm


class UserSignupView(View):
    """User signup view."""

    def get(self, request, *args, **kwargs):
        """Render user sign up form."""
        form = UserCreateForm()
        return render(request, "registration/signup.html", {"form": form})

    def post(self, request, *args, **kwargs):
        """Handle user sign up form submission."""
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
        return render(request, "registration/signup.html", {"form": form})
