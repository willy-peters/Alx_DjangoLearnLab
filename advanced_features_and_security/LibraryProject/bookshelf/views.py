# bookshelf/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import BookForm, BookSearchForm
from django.db.models import Q
from django.conf import settings

@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, "bookshelf/book_list.html", {"books": books})

@permission_required("bookshelf.can_create", raise_exception=True)
def create_book(request):
    # Example: Normally you'd use a form
    return HttpResponse("You have permission to create a book!")

@permission_required("bookshelf.can_edit", raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return HttpResponse(f"You can edit book: {book.title}")

@permission_required("bookshelf.can_delete", raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return HttpResponse(f"You can delete book: {book.title}")


# Example view using safe ORM
def search_books(request):
    query = request.GET.get('q', '')
    if query:
        # ORM automatically prevents SQL injection
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    else:
        books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

# Example view using Django forms to validate input
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()  # Safe, sanitized save
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})

def book_list(request):
    """
    Search and list books.
    Important security practices:
    - Use Django ORM to avoid SQL injection (no string formatting into queries).
    - Validate user input via forms.
    - Escape output in templates (Django auto-escapes).
    """
    form = BookSearchForm(request.GET or None)
    books = Book.objects.none()

    if form.is_valid():
        q = form.cleaned_data.get("q")
        if q:
            # Parameterized ORM query, safe from SQL injection
            books = Book.objects.filter(
                Q(title__icontains=q) | Q(author__icontains=q)
            ).distinct()
        else:
            books = Book.objects.all()

    context = {"books": books, "form": form}
    return render(request, "bookshelf/book_list.html", context)


def book_create(request):
    """
    Example of secure form handling for POST requests.
    - Uses Django ModelForm for validation and safe saving.
    - CSRF protection is enforced by CsrfViewMiddleware and {% csrf_token %}.
    """
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("bookshelf:book_list")
    else:
        form = BookForm()
    return render(request, "bookshelf/form_example.html", {"form": form})