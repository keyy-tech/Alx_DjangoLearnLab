from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import Library, Book
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def is_role(user):
    role = getattr(getattr(user, "profile", None), "role", None)
    if role == "admin":
        return True
    if role == "librarian":
        return True
    if role == "member":
        return True
    return False


def list_books(request):
    books = Book.objects.select_related("author").all()
    return render(request, "relationship_app/list_books.html", {"books": books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # only include books for this library
        context["books"] = Book.objects.filter(library=self.object)
        return context


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("list_books")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})


@login_required
@user_passes_test(is_role)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


@login_required
@user_passes_test(is_role)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


@login_required
@user_passes_test(is_role)
def member_view(request):
    return render(request, "relationship_app/member_view.html")
