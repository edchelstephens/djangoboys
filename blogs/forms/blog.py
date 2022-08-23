from django import forms

from blogs.models import Post


class PostForm(forms.ModelForm):
    """Post model form."""

    class Meta:
        model = Post
        fields = ("title", "text")
