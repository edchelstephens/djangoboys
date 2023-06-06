from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View

from blogs.models import Comment


class CommentApproveView(LoginRequiredMixin, View):
    """Comment approve view."""

    def get(self, request, pk, *args, **kwargs):
        """Handle post request."""
        comment = get_object_or_404(Comment, pk=pk)
        post = comment.post
        if not post.author == request.user:
            return Http404()
        else:
            comment.approve()
            return redirect("blogs:post_detail", pk=comment.post.pk)


class CommentDeleteView(LoginRequiredMixin, View):
    """Comment delete view."""

    def get(self, request, pk, *args, **kwargs):
        """Handle post request."""
        comment = get_object_or_404(Comment, pk=pk)
        post = comment.post
        if not post.author == request.user:
            return Http404()
        else:
            comment.delete()
            return redirect("blogs:post_detail", pk=comment.post.pk)
