from django.contrib import admin

from blogs.models import Post

class PostAdmin(admin.ModelAdmin):
    """Post model admin."""

    fields = [
        "author",
        "title",
        "text",
        "published_at"
    ]

    list_display = (
        "id",
        "author",
        "title",
        "text",
        "created_at",
        "published_at"
    )

admin.site.register(Post, PostAdmin)


    