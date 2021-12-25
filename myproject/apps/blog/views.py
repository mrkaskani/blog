from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from taggit.models import Tag

from .models import Post, Comment
from .forms import CommentForm, SearchForm


class About(generic.TemplateView):
    template_name = 'blog/about.html'


class PostListView(generic.ListView):
    model = Post
    queryset = Post.objects.filter(publish=True).order_by('-published_at')
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5


def post_detail_view(request, slug):
    post_detail = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.all().filter(post=post_detail.id).filter(approved_comment=True)

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post_detail
            comment.author = request.user
            comment.save()
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {
        'post_detail': post_detail, 'comments': comments, 'form': form,
    })


def tagged(request, tag_slug):
    tags = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tags)
    context = {
        'tags': tags,
        'posts': posts,
    }
    return render(request, 'blog/post_tags.html', context)


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    permission_required = 'blog.add_post', 'blog.change_comment'
    raise_exception = True
    template_name = 'blog/post_new.html'
    model = Post
    fields = ['title', 'slug', 'body', 'image', 'tags', 'publish']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form=form)


class UpdatePostView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Post
    fields = ['title', 'slug', 'body', 'image', 'tags', 'publish']
    template_name = 'blog/post_update.html'
    permission_required = 'blog.change_post'
    raise_exception = True

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(UpdatePostView, self).form_valid(form=form)


class DraftListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Post
    queryset = Post.objects.all().filter(publish__exact=False)
    template_name = 'blog/draft_list.html'
    permission_required = 'blog.can_view'
    raise_exception = True


class SearchPost(LoginRequiredMixin, generic.FormView, generic.ListView):
    template_name = 'blog/search.html'
    model = Post
    form_class = SearchForm
    context_object_name = 'search_results'

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('body', weight='A') + SearchVector('title', weight='A')
            search_query = SearchQuery(query)

            objects = Post.objects.filter(publish=True)
            search_result = objects.annotate(
                search=search_vector, rank=SearchRank(search_vector, search_query)
            ).filter(rank__gte=0.3).order_by('-rank')

            return search_result


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = 'blog.delete_post'
    raise_exception = True
