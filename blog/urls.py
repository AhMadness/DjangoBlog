# APP-LEVEL URLS

from django.urls import path
from . import views
from .views import (HomeView, AboutView, PostView, 
                    NewPostView, EditPostView, DeletePostView)

app_name = "blog"

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"), # path extends a function
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", views.contact_view, name="contact"),
    path("post/<int:pk>/", PostView.as_view(), name="post_detail"),
    path("new_post/", NewPostView.as_view(), name="new_post"),
    path("post/<int:pk>/edit/", EditPostView.as_view(), name="edit_post"),
    path("post/<int:pk>/remove/", DeletePostView.as_view(), name="remove_post"),
    path("category/<str:genre>/", views.CategoryView, name="categories"),
    path("profile/<str:username>/", views.ProfileView, name="user_posts"),
    path("post/like/<int:pk>/", views.LikeView, name="like_post"),
    path("post/<int:post_pk>/comment/<int:comment_pk>/remove/", views.delete_comment, name="remove_comment"),
    path("post/<int:post_pk>/comment/<int:comment_pk>/edit/", views.update_comment, name="edit_comment"),
    path("search/", views.search, name="search")
]
