from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy

from .forms import PostForm
from .models import Post
from django.contrib import messages


class PostListView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "post/post_lists.html"


class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "post/post_detail.html"


class PostCreateView(CreateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Post
    form_class = PostForm
    template_name = "post/post_create.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        messages.success(self.request, "Post created successfully")
        return super().form_valid(form)


class PostUpdateView(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Post
    form_class = PostForm
    template_name = "post/post_update.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully")
        return super().form_valid(form)


class PostDeleteView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = Post
    success_url = reverse_lazy("home")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Post deleted successfully")
        return super().delete(request, *args, **kwargs)
