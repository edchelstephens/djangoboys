from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import DetailView, TemplateView, View

from blogs.forms.post import PostForm
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


class PostDrafListView(LoginRequiredMixin, TemplateView):
    """Draf post lists template view."""

    template_name = "blogs/post_draft_lists.html"

    def get_posts(self) -> QuerySet:
        """Get unpublished posts up to this point."""
        posts = Post.objects.filter(published_at__isnull=True).order_by("created_at")

        return posts

    def get_context_data(self, **kwargs) -> dict:
        """Get context to be rendered on template."""
        context = super().get_context_data(**kwargs)
        context["posts"] = self.get_posts()
        return context


class PostView(LoginRequiredMixin, View):
    """Post view."""

    def get(self, request, *args, **kwargs):
        form = PostForm()
        return render(
            request, template_name="blogs/post_edit.html", context={"form": form}
        )

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect("blogs:post_detail", pk=post.pk)


class PostDeleteView(LoginRequiredMixin, View):
    """Post delete view."""

    def get(self, request, pk: int, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return redirect("blogs:post_list")


class PostEditView(LoginRequiredMixin, View):
    """Post edit view."""

    def get(self, request, pk: int, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(instance=post)
        return render(
            request, template_name="blogs/post_edit.html", context={"form": form}
        )

    def post(self, request, pk: int, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect("blogs:post_detail", pk=post.pk)


class PostDetailView(DetailView):
    """PostDetailView."""

    template_name = "blogs/post_detail.html"
    model = Post


class PostPublishView(LoginRequiredMixin, View):
    """Post publish view."""

    def get(self, request, pk: int, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        post.publish()
        return redirect("blogs:post_detail", pk=pk)
