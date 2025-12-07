from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages

from .forms import LoginForm, RegisterForm


# Create your views here.
def create_user(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect("login")
        messages.warning(request, "Error creating account.Please try again")
    context = {"form": form}
    return render(request, "user/signup.html", context)


def login_view(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            messages.success(request, "Logged in successfully")
        messages.error(request, "Invalid username or password")
        return redirect("home")
    context = {"form": form}
    return render(request, "user/login.html", context)


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("login")


@login_required
def profile_view(request):
    context = {"users": request.user}
    return render(request, "user/profile.html", context)


@login_required
def update_profile(request):
    form = RegisterForm(instance=request.user)
    if request.method == "POST":
        form = RegisterForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("profile")
        messages.warning(request, "Error updating profile. Please try again")
    context = {"form": form}
    return render(request, "user/update_profile.html", context)


@login_required
def delete_account(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")

        if str(request.user.id) != str(user_id):
            messages.warning(request, "Error deleting account. Please try again")
            return redirect("profile")

        request.user.delete()
        messages.success(request, "Account deleted successfully")
        return redirect("home")

    context = {"user": request.user}
    return render(request, "user/delete_account.html", context)
