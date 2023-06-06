from django import forms

from blogs.models import Comment


class CommentForm(forms.ModelForm):
    """Comment Form."""

    class Meta:
        model = Comment
        fields = ("author", "text")
