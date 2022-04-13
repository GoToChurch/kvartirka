from rest_framework.response import Response
from rest_framework import viewsets, permissions, pagination, generics
from .models import *
from .serializers import BlogSerializer, PostSerializer, UserSerializer, \
    SubscribeSerializer, SeenPostSerializer, CommentSerializer


class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    ordering = 'created_at'


class BlogsView(viewsets.ModelViewSet):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
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

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'url'
    pagination_class = PageNumberSetPagination


class SubscribeView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        username = self.kwargs['username'].lower()
        return Subscribe.objects.filter(subscriber=username)


class SeenPostsView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = SeenPosts.objects.all()
    serializer_class = SeenPostSerializer

    def get_queryset(self):
        username = self.kwargs['username'].lower()
        return SeenPosts.objects.filter(user=username)

class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_slug = self.kwargs['post_slug'].lower()
        post = Post.objects.get(slug=post_slug)
        return Comment.objects.filter(post=post)