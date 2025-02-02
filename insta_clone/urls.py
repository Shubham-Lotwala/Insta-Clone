from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from post.views import *
from users.views import *
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view, name="home"),
    path("post/create/", post_create_view, name="post-create"),
    path("post/delete/<pk>/", post_delete_view, name="post-delete"),
    path("post/edit/<pk>/", post_edit_view, name="post-edit"),
    path("post/<pk>/", post_page_view, name="post-page"),
    path("accounts/", include("allauth.urls")),
    path("profile/", profile_view, name="profile"),
    path("profile.edit/", profile_edit_view, name="profile-edit"),
    path("<username>/", profile_view, name="display-profile"),
    path("commentsent/<pk>/", comment_sent, name="comment-sent"),
    path("comment/delete/<pk>/", comment_delete_view, name="comment-delete"),
    path("reply-sent/<pk>/", reply_sent, name="reply-sent"),
    path("reply-delete/<pk>/", reply_delete_view, name="reply-delete"),
    path("post/like/<pk>", like_post_view, name="like-post"),
    path("comment/like/<pk>", like_comment_view, name="like-comment"),
    path("reply/like/<pk>", like_reply_view, name="like-reply"),
    path("sidebar/", sidebar_view, name="sidebar"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
