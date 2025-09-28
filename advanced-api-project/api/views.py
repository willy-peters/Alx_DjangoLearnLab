from rest_framework import generics, permissions, filters
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework


# ----------------------------
# CRUD Views for Book model
# ----------------------------

class BookListView(generics.ListAPIView):
    """
    Retrieve a list of all books.
    Open to everyone (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can read


    # Filtering, Searching, Ordering setup
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Filter by fields
    filterset_fields = ['title', 'author__name', 'publication_year']

    # Search in fields (partial matches)
    search_fields = ['title', 'author__name']

    # Allow ordering by fields
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # Default ordering


class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieve details of a single book by ID.
    Open to everyone (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    Create a new book.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Extra hook for customization (future extension, e.g. assign request.user)
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    Update an existing book.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # Extra hook to enforce validation or log updates
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    Delete a book.
    Restricted to authenticated users only.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


# Book API Query Features

## Filtering
"""
- `/api/books/?publication_year=1949` → Filter by year
- `/api/books/?author__name=George Orwell` → Filter by author

## Searching
- `/api/books/?search=Farm` → Search in title or author name

## Ordering
- `/api/books/?ordering=title` → Order alphabetically
- `/api/books/?ordering=-publication_year` → Order by year descending
"""