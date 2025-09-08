from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


# ----------------------------
# Function-based View
# ----------------------------
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


# ----------------------------
# Class-based View
# ----------------------------
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

# User login view
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("list_books")  # redirect wherever you want
    else:
        form = AuthenticationForm()
    return render(request, "relationship_app/login.html", {"form": form})

# User logout view
def user_logout(request):
    logout(request)
    return render(request, "relationship_app/logout.html")

# User registration view
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login after registration
            return redirect("list_books")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})