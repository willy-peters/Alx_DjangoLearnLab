# bookshelf/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.conf import settings

from .models import Book
from .forms import BookForm, BookSearchForm, ExampleForm   # ✅ Added ExampleForm


@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, "bookshelf/book_list.html", {"books": books})


@permission_required("bookshelf.can_create", raise_exception=True)
def create_book(request):
    return HttpResponse("You have permission to create a book!")


@permission_required("bookshelf.can_edit", raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return HttpResponse(f"You can edit book: {book.title}")


@permission_required("bookshelf.can_delete", raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return HttpResponse(f"You can delete book: {book.title}")


def search_books(request):
    query = request.GET.get("q", "")
    if query:
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    else:
        books = Book.objects.all()
    return render(request, "bookshelf/book_list.html", {"books": books})


def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm()
    return render(request, "bookshelf/form_example.html", {"form": form})


def example_form_view(request):
    """
    Demonstrates secure form handling with ExampleForm.
    - Uses CSRF token (enforced by middleware + template tag).
    - Validates input with Django forms.
    """
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            author = form.cleaned_data["author"]
            return HttpResponse(f"Received: {title} by {author}")
    else:
        form = ExampleForm()

    return render(request, "bookshelf/form_example.html", {"form": form})
