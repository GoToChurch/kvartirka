from rest_framework.response import Response
from rest_framework import generics, permissions, pagination, viewsets

from .models import Blog, Comment, Post, SeenPosts, Subscribe
from .serializers import BlogSerializer, CommentSerializer, PostSerializer,\
    SeenPostSerializer, SubscribeSerializer, UserSerializer


class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    ordering = 'created_at'


class BlogsView(viewsets.ModelViewSet):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    lookup_field = 'url'
    pagination_class = PageNumberSetPagination


class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_url = self.kwargs['post_url'].lower()
        post = Post.objects.get(url=post_url)
        return Comment.objects.filter(post=post)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'url'
    pagination_class = PageNumberSetPagination


class ProfileView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return Response({
            "user": UserSerializer(request.user,
                                   context=self.get_serializer_context()).data,
        })

class ReplyView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        parent_id = self.kwargs['parent_id'].lower()
        return Comment.objects.filter(parent_id=parent_id)


class SeenPostsView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = SeenPosts.objects.all()
    serializer_class = SeenPostSerializer

    def get_queryset(self):
        username = self.kwargs['username'].lower()
        return SeenPosts.objects.filter(user=username)


class SubscribeView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        username = self.kwargs['username'].lower()
        return Subscribe.objects.filter(subscriber=username)
