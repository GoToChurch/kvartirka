from django.contrib.auth import login, authenticate
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from .forms import CommentForm, LogInForm, PostForm
from .models import Blog, Comment, Post, SeenPosts, Subscribe


class MainView(View):
    '''Представление домашней страницы'''

    def get(self, request, *args, **kwargs):
        return render(
            request, 'test_blog/home.html')


class HomeBlogView(View):
    '''Представление блога активного пользователя'''

    def get(self, request, *args, **kwargs):
        user = request.user
        blog = get_object_or_404(Blog, author=user) # Нужно для шаблона
        self_blog = get_object_or_404(Blog, author=user) # Используется в шаблоне,
        # когда сравниваются просматриваемый блог и блог активного пользователя
        posts = Post.objects.all().filter(author=user) # Все посты блога активного пользователя
        paginator = Paginator(posts, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'test_blog/blog.html', context={
            'blog': blog,
            'self_blog': self_blog,
            'page_obj': page_obj
        })

class BlogsView(View):
    '''Представление блогов, на которые может подписаться активный пользователь'''

    def get(self, request, *args, **kwargs):
        blogs = Blog.objects.all().exclude(author=request.user) # Выбираем все блоги,
        # кроме блога активного пользователя
        paginator = Paginator(blogs, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'test_blog/blogs.html', context={
            'page_obj': page_obj
        })


class OtherBlogView(View):
    '''Представление блога другого пользователя'''

    def get(self, request, slug, *args, **kwargs):
        user = request.user
        blog = get_object_or_404(Blog, url=slug)
        self_blog = get_object_or_404(Blog, author=user) # Используется в шаблоне,
        # когда сравниваются просматриваемый блог и блог активного пользователя
        posts = Post.objects.all().filter(blog=blog)
        paginator = Paginator(posts, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        subscribed = Subscribe.objects.filter(subscriber=user, blog=blog).exists()
        return render(request, 'test_blog/other_blog.html', context={
            'self_blog': self_blog,
            'blog': blog,
            'page_obj': page_obj,
            'subscribed': subscribed
        })


class SubscribeView(View):
    '''Представление для подписки на блог'''

    def get(self, request, slug, *args, **kwargs):
        blog = Blog.objects.get(url=slug)
        user = request.user
        subscribed_blogs = Subscribe.objects.only('blog').\
            filter(subscriber=user).values_list('blog')
        if not blog in subscribed_blogs:
            Subscribe.objects.get_or_create(subscriber=user, blog=blog)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class UnsubscribeView(View):
    '''Представление для отписки от блога'''

    def get(self, request, slug, *args, **kwargs):
        blog = Blog.objects.get(url=slug)
        Subscribe.objects.get(subscriber=request.user, blog=blog).delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class FeedView(View):
    '''Представление ленты новостей активного пользователя'''

    def get(self, request, *args, **kwargs):
        user = request.user
        blogs = user.subscriber.values_list('blog', flat=True) # Выбираем все блоги,
        # на которые подписан пользователь
        posts = Post.objects.all().filter(blog__in=blogs).order_by('created_at')
        paginator = Paginator(posts, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'test_blog/feed.html', context={
            'user': user,
            'page_obj': page_obj
        })


class PostView(View):
    '''Представление одного поста блога'''

    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, url=slug)
        seen = SeenPosts.objects.filter(user=request.user, post=post).exists()
        comment_form = CommentForm()
        comments = post.comments.filter(parent__isnull=True)
        return render(request, 'test_blog/post.html', context={
            'comment_form': comment_form,
            'comments': comments,
            'post': post,
            'seen': seen
        })

    def post(self, request, slug, *args, **kwargs):
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                if parent_obj:
                    reply_comment = comment_form.save(commit=False)
                    reply_comment.parent = parent_obj
            new_comment = comment_form.save(commit=False)
            new_comment.username = self.request.user
            new_comment.post = get_object_or_404(Post, url=slug)
            new_comment.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return render(request, 'test_blog/post.html', context={
            'comment_form': comment_form,
        })

class PostCreateView(View):
    '''Представление формы создания поста'''

    def get(self, request, *args, **kwargs):
        form = PostForm()
        return render(request, 'test_blog/new_post.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            blog = get_object_or_404(Blog, author=request.user)
            post.blog = blog
            post.save()
            return redirect('/')
        return render(request, 'test_blog/new_post.html', context={
            'form': form,
        })


class SeenPostView(View):
    '''Представление для отметки просмотра поста'''

    def get(self, request, slug, *args, **kwargs):
        post = Post.objects.get(url=slug)
        user = request.user
        seen_posts = SeenPosts.objects.only('post').filter(
            user=user).values_list('post')
        if not post in seen_posts:
            SeenPosts.objects.get_or_create(user=user, post=post)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class LogInView(View):
    '''Представление форма входа на сайт'''

    def get(self, request, *args, **kwargs):
        form = LogInForm()
        return render(request, 'test_blog/login.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = LogInForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'test_blog/login.html', context={
            'form': form,
        })
