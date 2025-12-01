from django.contrib.auth import logout
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib import messages

# Create your views here.
def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
    context = {"form": form}
    return render(request, "blog/register.html", context)


def login_view(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            messages.success(request, "Logged in successfully")
        messages.error(request, "Invalid username or password")
    context = {"form": form}
    return render(request, "blog/login.html", context)

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("login")