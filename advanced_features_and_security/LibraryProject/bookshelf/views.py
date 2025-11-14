from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .forms import BookForm
from .models import Book
from django.contrib.auth.decorators import permission_required
from .forms import ExampleForm


# Create your views here.
@permission_required("bookshelf.view_book", raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, "bookshelf/book_list.html", {"books": books})


@permission_required("bookshelf.create_book", raise_exception=True)
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book created successfully")
            return redirect("book_list")
    else:
        form = BookForm()
        messages.error(request, "Please fill in the form to create a new book")
    return render(request, "bookshelf/book_create.html", {"form": form})


@permission_required("bookshelf.create_book", raise_exception=True)
def form_example(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book created successfully")
            return redirect("book_list")
    else:
        form = BookForm()
        messages.error(request, "Please fill in the form to create a new book")
    return render(request, "bookshelf/form_example.html", {"form": form})


@permission_required("bookshelf.change_book", raise_exception=True)
def book_update(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated successfully")
            return redirect("book_list")
    else:
        form = BookForm(instance=book)
        messages.error(request, "Please fill in the form to update the book")
    return render(request, "bookshelf/book_update.html", {"form": form})


@permission_required("bookshelf.delete_book", raise_exception=True)
def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    messages.success(request, "Book deleted successfully")
    return redirect("book_list")
