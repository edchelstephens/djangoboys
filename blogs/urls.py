from django.urls import path

from blogs.views.post import PostListTemplateView, PostDetailView, PostView

app_name = "blogs"

urlpatterns = [
    path("", PostListTemplateView.as_view(), name="post_list"),
    path("post/new/", PostView.as_view(), name="post_new"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
]
