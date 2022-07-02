from django.urls import path

from blogs.views.post import PostListTemplateView

app_name = "blogs"

urlpatterns = [path("", PostListTemplateView.as_view(), name="post_list")]
