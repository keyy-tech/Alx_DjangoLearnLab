from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Post, Comment
from .forms import PostForm, CommentForm


# ---------------- POST VIEWS ----------------
class PostListView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "post/../templates/blog/post_lists.html"


class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "post/../templates/blog/post_detail.html"


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "post/../templates/blog/post_form.html"
    success_url = reverse_lazy("post_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post created successfully")
        return super().form_valid(form)

    def test_func(self):
        return True  # any logged-in user can create


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "post/../templates/blog/post_update.html"
    success_url = reverse_lazy("post_list")

    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully")
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("post_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Post deleted successfully")
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        return self.get_object().author == self.request.user


# ---------------- COMMENT VIEWS ----------------
class CommentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "comments/../templates/blog/comment_create.html"

    def form_valid(self, form):
        post = Post.objects.get(pk=self.kwargs.get("post_id"))
        form.instance.post = post
        form.instance.author = self.request.user
        messages.success(self.request, "Comment created successfully")
        return super().form_valid(form)

    def test_func(self):
        return True

    def get_success_url(self):
        return self.object.post.get_absolute_url()


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "comments/../templates/blog/comment_update.html"

    def form_valid(self, form):
        messages.success(self.request, "Comment updated successfully")
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return self.object.post.get_absolute_url()


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Comment deleted successfully")
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return self.object.post.get_absolute_url()
