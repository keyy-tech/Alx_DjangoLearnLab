from django.shortcuts import render
from .models import Book
from django.views.generic import DetailView, ListView


def list_all_books(request):
    books = Book.objects.select_related("author").all()
    return render(request, "relationship_app/list_books.html", {"books": books})


class DetailLibraryList(DetailView):
    model = Book
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = Book.objects.all()
        return context
