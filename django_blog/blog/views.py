from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.urls import reverse_lazy, reverse
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment, Tag
from .forms import PostForm
from django.shortcuts import get_object_or_404
from .forms import CommentForm
from django.db.models import Q



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optionally log the user in immediately:
            login(request, user)
            messages.success(request, f'Account created for {user.username}.')
            return redirect('blog:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile(request):
    # view & edit profile in same view
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('blog:profile')  # Post/Redirect/Get pattern
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'blog/profile.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'   # blog/templates/blog/post_list.html
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5  # optional

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # comments for the post
        ctx['comments'] = self.object.comments.all()
        # form for new comment (rendered inline on post detail)
        ctx['comment_form'] = CommentForm()
        return ctx

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    # where to redirect on success:
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    

# Create a comment attached to a given post (URL will supply post_pk)
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'  # fallback standalone form

    def dispatch(self, request, *args, **kwargs):
        self.post = get_object_or_404(Post, pk=kwargs.get('post_pk'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post-detail', kwargs={'pk': self.post.pk})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse('blog:post-detail', kwargs={'pk': self.get_object().post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse('blog:post-detail', kwargs={'pk': self.get_object().post.pk})
    

# Posts by tag
class PostsByTagListView(ListView):
    model = Post
    template_name = 'blog/posts_by_tag.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        tag_name = self.kwargs.get('tag_name')
        return Post.objects.filter(tags__name__iexact=tag_name).order_by('-published_date')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['tag_name'] = self.kwargs.get('tag_name')
        return ctx




# Search view (function-based for simplicity)
from django.views.decorators.http import require_GET

@require_GET
def search_results(request):
    q = request.GET.get('q', '').strip()
    results = Post.objects.none()
    if q:
        results = Post.objects.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(tags__name__icontains=q)
        ).distinct().order_by('-published_date')
    context = {'query': q, 'results': results}
    return render(request, 'blog/search_results.html', context)