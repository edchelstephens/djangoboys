from django.db import models
from django.db.models import QuerySet
from django.utils import timezone


class Post(models.Model):
    """Blog post model."""

    author = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    published_at = models.DateTimeField(blank=True, null=True)

    def __repr__(self) -> str:
        """Python object string representation."""
        return "Post(id={}, title={}, author={})".format(
            self.id, self.title, repr(self.author)
        )

    def __str__(self) -> str:
        """Human readable string representation."""
        return self.title

    def publish(self) -> None:
        """Publish the post."""
        self.published_at = timezone.now()
        self.save()

    def is_published(self) -> bool:
        """Check if post is published by checking the published_at datetime field."""
        return self.published_at is not None

    def approved_comments(self) -> QuerySet:
        """Get queryset of approved comments."""
        return self.comments.filter(is_approved=True)
