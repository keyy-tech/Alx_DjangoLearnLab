from django.shortcuts import render
from django.views.generic import CreateView

from .models import Library
from django.views.generic.detail import DetailView
from .models import Book
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def list_books(request):
    books = Book.objects.select_related("author").all()
    return render(request, "relationship_app/list_books.html", {"books": books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = Book.objects.all()
        return context


class UserRegisterView(CreateView):
    template_name = "relationship_app/register.html"
    form_class = UserCreationForm
    success_url = "list_all_books"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
