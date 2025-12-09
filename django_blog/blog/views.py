from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, PostForm, CommentForm
from .models import Post, Comment
from django.db.models import Q

# ----------------------------
# USER VIEWS
# ----------------------------


def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect("login")

    return render(request, "blog/register.html", {"form": form})


def login_view(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            messages.success(request, "Logged in successfully")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "blog/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("login")


@login_required
def profile_view(request):
    return render(request, "blog/profile.html", {"users": request.user})


@login_required
def update_profile(request):
    form = RegisterForm(instance=request.user)

    if request.method == "POST":
        form = RegisterForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("profile")

    return render(request, "blog/update_profile.html", {"form": form})


@login_required
def delete_account(request):
    request.user.delete()
    return redirect("login")


# ----------------------------
# POST VIEWS
# ----------------------------


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "blog/post_form.html"
    form_class = PostForm
    model = Post
    success_url = reverse_lazy("blog:post-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    template_name = "blog/post_update.html"
    form_class = PostForm
    model = Post
    success_url = reverse_lazy("blog:post-list")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    template_name = "blog/post_delete.html"
    model = Post
    success_url = reverse_lazy("blog:post-list")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostListView(generic.ListView):
    template_name = "blog/post_lists.html"
    model = Post
    context_object_name = "posts"

    def get_queryset(self):
        query = self.request.GET.get("q")
        tag = self.request.GET.get("tag")

        queryset = Post.objects.all().order_by("-published_date")

        if query:
            queryset = Post.objects.filter(
                Q(title__icontains=query)
                | Q(content__icontains=query)
                | Q(author__username__icontains=query)
            )

        if tag:
            queryset = queryset.filter(tags__name__icontains=tag)

        return queryset


class PostDetailView(generic.DetailView):
    template_name = "blog/post_detail.html"
    model = Post
    context_object_name = "post"


# ----------------------------
# COMMENT VIEWS
# ----------------------------


class CommentCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "blog/comment_create.html"
    form_class = CommentForm
    model = Comment

    def form_valid(self, form):
        post_id = self.kwargs["pk"]
        post = get_object_or_404(Post, pk=post_id)

        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:post-detail", kwargs={"pk": self.kwargs["pk"]})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    template_name = "blog/comment_update.html"
    form_class = CommentForm
    model = Comment

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse("blog:post-detail", kwargs={"pk": self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Comment

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse("blog:post-detail", kwargs={"pk": self.object.post.pk})


class CommentListView(generic.ListView):
    template_name = "blog/comment_lists.html"
    model = Comment
