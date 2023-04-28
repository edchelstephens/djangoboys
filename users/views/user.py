from django.contrib.auth import login
from django.shortcuts import redirect, render

from users.forms.user import UserCreateForm
from users.models.user import User
from utils.views import DjangoView


class UserSignupView(DjangoView):
    """User signup view."""

    def get(self, request, *args, **kwargs):
        """Render user sign up form."""
        form = UserCreateForm()
        return render(request, "registration/signup.html", {"form": form})

    def validate(self, data: dict) -> bool:
        """Validate signup data."""
        is_valid = False
        validation_message = ""

        email = data.get("email")
        username = data.get("username")
        password = data.get("password")
        password2 = data.get("password2")

        if User.objects.filter(email=email).exists():
            validation_message = "Email unavailable."
        elif User.objects.filter(username=username).exists():
            validation_message = "Username unavailable."
        elif password != password2:
            validation_message = "Passwords do not match."
        else:
            is_valid = True

        return is_valid, validation_message

    def post(self, request, *args, **kwargs):
        """Handle user sign up form submission."""
        data = request.POST
        is_valid, signup_error = self.validate(data)
        form = UserCreateForm(data)
        if is_valid:
            if form.is_valid():
                user = form.save()
                user.set_password(data.get("password"))
                user.save()
                login(request, user)

                return redirect("/")
        else:
            context = {"form": form, "signup_error": signup_error}
            return render(request, "registration/signup.html", context=context)
