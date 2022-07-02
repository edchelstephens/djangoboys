from django.views.generic import TemplateView

class PostListTemplateView(TemplateView):
    """Post lists template view."""
    template_name = "blogs/post_lists.html"

    