from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import date
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import post, like, comment, categories
from .forms import CommentForm
from . import serializers
# Create your views here.

def BlogHomeView(request):
    all_categories = categories.objects.all()
    all_posts = post.objects.order_by('-date')
    search_term = ''
    recent_posts = all_posts[:4]

    if 'category' in request.GET:
        selected_category_title = request.GET.get('category')
        all_posts = all_posts.filter(category__title = selected_category_title)
    
    if 'search' in request.GET:
        search_term = request.GET['search']
        print(search_term)
        all_posts = all_posts.filter(Q(title__icontains = search_term)| Q(content__contains=search_term))

    paginator = Paginator(all_posts, 5)

    page = request.GET.get('page')
    all_posts = paginator.get_page(page)

    get_dict_copy = request.GET.copy()
    params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
    context = {
        'categories': all_categories,
        'posts': all_posts,
        'params': params, 
        'search_term': search_term,
        'recent_posts':recent_posts,
    }
    return render(request, 'bloghome.html', context)


def BlogPostView(request, id):

    slug_post = get_object_or_404(post, id = id)
    comments = comment.objects.filter(post = slug_post)
    all_categories = categories.objects.all()
    recent_posts = post.objects.order_by('-date')[:4]
    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                new_comment = comment()
                new_comment.comment_text = form.cleaned_data.get('comment_text')
                new_comment.name = form.cleaned_data.get('name')
                new_comment.post = slug_post
                new_comment.date = date.today()
                new_comment.user = request.user
                new_comment.save()
                messages.success(
                                request,
                                'Comment Added Successfully',
                                extra_tags='alert alert-success alert-dismissible fade show'
                                )
                return redirect('blog:post', id)
        else:
            messages.success(
                                request,
                                'Login to leave a comment',
                                extra_tags='alert alert-success alert-dismissible fade show'
                                )
            return redirect('blog:post', id)
    else:
        form = CommentForm()
        context = {
            'commentform': form,
            'post': slug_post,
            'comments': comments,
            'categories': all_categories,
            'recent_posts':recent_posts,
        }
        return render(request, 'blogpost.html', context)



class CategoriesAPIViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CategoriesSerializer
    queryset = categories.objects.all()

    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class BlogPostAPIViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BlogPostSerializer
    queryset = post.objects.all()

    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


class BlogPostCommentAPIViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BlogPostCommentSerializer
    queryset = comment.objects.all()

    def get_permissions(self):
        permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

