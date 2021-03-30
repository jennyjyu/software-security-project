from django.urls import path, include
from comments.models import Comment, Like
from comments.views import CommentList, CommentDetail, LikeList, LikeDetail
from rest_framework.urlpatterns import format_suffix_patterns
from users import views

urlpatterns = [
    path("api/comments/", CommentList.as_view(), name="comment-list"),
    path("api/comments/<int:pk>/", CommentDetail.as_view(), name="comment-detail"),
    path("api/likes/", LikeList.as_view(), name="like-list"),
    path("api/likes/<int:pk>/", LikeDetail.as_view(), name="like-detail"),
    path("api/activate/<str:uidb64>/<str:token>/", views.activate, name='activate'),
]