from django.contrib import admin

from blogs.models import Comment


class CommentAdmin(admin.ModelAdmin):
    """Comment model admin."""

    fields = [
        "post",
        "author",
        "text",
        "created_at",
        "is_approved",
    ]

    list_display = [
        "id",
        "post",
        "author",
        "text",
        "created_at",
        "is_approved",
    ]


admin.site.register(Comment, CommentAdmin)
