from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from taggit.models import Tag
from .models import Post, Comment
from .forms import PostForm, CommentForm


def about_me(request):
    return render(request, 'blog/about.html')


def post_list(request, tag_slug=None):
    # Add tags
    object_list = Post.objects.filter(publish=True).order_by('-published_at')
    tags = None

    if tag_slug:
        tags = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tags])

    # Add pagination
    paginator = Paginator(object_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.html', {'page_obj': posts, 'tags': tags})


def post_detail_view(request, slug):
    post_detail = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.all().filter(post=post_detail.pk).filter(approved_comment=True)

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post_detail
            comment.author = request.user
            comment.save()
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post_detail': post_detail, 'comments': comments, 'form': form})


@permission_required('blog.add_post', 'blog.change_comment', raise_exception=True)
@login_required()
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(reverse('blog:post_list'))
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form})


@permission_required('blog.change_post', raise_exception=True)
@login_required()
def update_post(request, slug):
    post_update = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, instance=post_update)
    if form.is_valid():
        tmp = form.save(commit=False)
        tmp.author = request.user
        tmp.updated_at = timezone.now()
        tmp.save()
        return redirect(reverse('blog:post_list'))
    return render(request, 'blog/post_update.html', {'form': form})


@permission_required('blog.delete_post', raise_exception=True)
@login_required()
def delete_post(request, slug):
    post_delete = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        post_delete.delete()
        return redirect(reverse('blog:post_list'))
    return render(request, 'blog/post_confirm_delete.html', {'object': post_delete})


@permission_required('blog.can_view', raise_exception=True)
@login_required()
def draft_list_view(request):
    posts = Post.objects.all().filter(publish__exact=False)
    return render(request, 'blog/draft_list.html', {'posts': posts})
