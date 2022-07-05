from django.views.generic import TemplateView, DetailView
from django.utils import timezone
from django.db.models import QuerySet

from blogs.models.post import Post


class PostListTemplateView(TemplateView):
    """Post lists template view."""

    template_name = "blogs/post_lists.html"

    def get_posts(self) -> QuerySet:
        """Get published posts up to this point."""
        posts = Post.objects.filter(published_at__lte=timezone.now()).order_by(
            "published_at"
        )
        return posts

    def get_context_data(self, **kwargs) -> dict:
        """Get context to be rendered on template."""
        context = super().get_context_data(**kwargs)
        context["posts"] = self.get_posts()
        return context


class PostDetailView(DetailView):
    """PostDetailView."""

    template_name = "blogs/post_detail.html"
    model = Post
