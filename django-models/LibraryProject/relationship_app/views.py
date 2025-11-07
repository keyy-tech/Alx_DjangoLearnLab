from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import Library, Book
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def _get_user_role(user):
    return getattr(getattr(user, "userprofile", None), "role", None)


def is_admin(user):
    return _get_user_role(user) == "admin"


def is_librarian_or_admin(user):
    return _get_user_role(user) in ("admin", "librarian")


def is_member_or_higher(user):
    return _get_user_role(user) in ("admin", "librarian", "member")


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
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


@login_required
@user_passes_test(is_librarian_or_admin)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


@login_required
@user_passes_test(is_member_or_higher)
def member_view(request):
    return render(request, "relationship_app/member_view.html")