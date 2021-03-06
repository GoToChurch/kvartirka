from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import BlogView, BlogsView, FeedView, LogInView, MainView, PostView, \
    PostCreateView, SeenPostView, SubscribeView, UnsubscribeView


urlpatterns = [
    path('', MainView.as_view(), name='home'),
    path('blog/<slug>/', BlogView.as_view(), name='blog'),
    path('blogs/', BlogsView.as_view(), name='blogs'),
    path('blog/<slug>/subscribe', SubscribeView.as_view(), name='subscribe'),
    path('blog/<slug>/unsubscribe', UnsubscribeView.as_view(), name='unsubscribe'),
    path('feed/', FeedView.as_view(), name='feed'),
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(),
         {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('new_post/', PostCreateView.as_view(), name='new_post'),
    path('post/<slug>/', PostView.as_view(), name='post'),

    path('post/<slug>/seen', SeenPostView.as_view(), name='seen_post'),
]
