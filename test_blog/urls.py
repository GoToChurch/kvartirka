from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import MainView, HomeBlogView, LogInView, PostView, BlogsView, \
    OtherBlogView, FeedView, PostCreateView, SubscribeView, UnsubscribeView, \
    SeenPostView


urlpatterns = [
    path('', MainView.as_view(), name='home'),
    path('blog/', HomeBlogView.as_view(), name='blog'),
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(),
         {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('blog/post/<slug>/', PostView.as_view(), name='post'),
    path('blog/post/<slug>/seen', SeenPostView.as_view(), name='seen_post'),
    path('other_blogs/', BlogsView.as_view(), name='blogs'),
    path('other_blog/<slug>/', OtherBlogView.as_view(), name='other_blog'),
    path('other_blog/<slug>/subscribe', SubscribeView.as_view(), name='subscribe'),
    path('other_blog/<slug>/unsubscribe', UnsubscribeView.as_view(), name='unsubscribe'),
    path('feed/', FeedView.as_view(), name='feed'),
    path('new_post/', PostCreateView.as_view(), name='new_post'),
]
