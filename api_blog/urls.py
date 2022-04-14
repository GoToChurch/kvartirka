from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import PostViewSet, BlogsView, ProfileView, SeenPostsView, \
    SubscribeView, CommentView, ReplyView


router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('blogs', BlogsView, basename='blogs')

urlpatterns = [
    path('', include(router.urls)),
    path('comments/', CommentView.as_view()),
    path('comments/<slug:post_url>/', CommentView.as_view()),
    path('replies/<slug:parent_id>/', ReplyView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('seen_posts/', SeenPostsView.as_view()),
    path('seen_posts/<slug:username>/', SeenPostsView.as_view()),
    path('subscribe/', SubscribeView.as_view()),
    path('subscribe/<slug:username>/', SubscribeView.as_view()),
]
