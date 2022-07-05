from django.urls import path

from blogs.views.post import PostListTemplateView, PostDetailView

app_name = "blogs"

urlpatterns = [
    path("", PostListTemplateView.as_view(), name="post_list"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
]
