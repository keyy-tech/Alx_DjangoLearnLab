from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from .forms import BookForm
from .models import  Book
from django.contrib.auth.decorators import permission_required,login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404


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

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("list_books")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    context = {"form": form}
    return render(request, "relationship_app/login.html", context)


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")



def is_admin(user):
    return user.is_authenticated and hasattr(user, "profile") and user.profile.role == "admin"

def is_librarian(user):
    return user.is_authenticated and hasattr(user, "profile") and user.profile.role == "librarian"

def is_member(user):
    return user.is_authenticated and hasattr(user, "profile") and user.profile.role == "member"


@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


@login_required
@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")


@login_required
@permission_required('relationship_app.can_view_book')
def book_list(request):
    books = Book.objects.select_related("authors").all()
    context = {"books": books}
    return render(request,"relationship_app/list_books.html",context)

@login_required
@permission_required('relationship_app.can_add_book')
def create_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book created successfully")
            return redirect("book_list")
    form = BookForm()
    messages.info(request, "Please fill in the form to create a new book")
    context = {"form": form}
    return render(request,"relationship_app/create_book.html",context)


@login_required
@permission_required('relationship_app.can_change_book')
def update_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated successfully")
            return redirect("book_list")
    form = BookForm(instance=book)
    messages.error(request, "Please fill in the form to update the book")
    context = {"form":form}
    return render(request,"relationship_app/update_book.html",context)

@login_required
@permission_required('relationship_app.can_delete_book')
def delete_view(request,book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    messages.success(request, "Book deleted successfully")
    return redirect("book_list")