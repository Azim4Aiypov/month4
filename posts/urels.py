from django.urls import path
from .views import posts_list_view, post_detail_view, post_create_view

urlpatterns = [
    path("", posts_list_view, name="posts_list_view"),
    path("<int:post_id>/", post_detail_view, name="post_detail_view"),
    path("create/", post_create_view, name="post_create_view"),
]
