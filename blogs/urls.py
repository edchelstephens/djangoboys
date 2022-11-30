from django.urls import path

from blogs.views import post

app_name = "blogs"

urlpatterns = [
    path("", post.PostListTemplateView.as_view(), name="post_list"),
    path("post/new/", post.PostView.as_view(), name="post_new"),
    path("post/<int:pk>/", post.PostDetailView.as_view(), name="post_detail"),
    path("post/<int:pk>/edit/", post.PostEditView.as_view(), name="post_edit"),
    path("post/drafts/", post.PostDrafListView.as_view(), name="post_draft_list"),
]
