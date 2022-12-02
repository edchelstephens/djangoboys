from django.db import models
from django.utils import timezone


class Comment(models.Model):
    """Comment on blog post model."""

    post = models.ForeignKey(
        "blogs.Post", on_delete=models.CASCADE, related_name="comments"
    )
    author = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __repr__(self) -> str:
        """Return python object representation."""
        return f"Comment(id={self.id}, post={self.post}, text={self.text}, author={self.author})"

    def __str__(self) -> str:
        """Human readable string representation."""
        return self.text

    def approve(self) -> None:
        """Approve the comment."""
        self.is_approved = True
        self.save()
