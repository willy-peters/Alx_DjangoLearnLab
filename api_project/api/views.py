from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Book
from .serializers import BookSerializer


# BookViewSet:
# - Uses TokenAuthentication (configured in settings.py)
# - Requires user authentication for all actions
# - Permissions can be adjusted (e.g., IsAdminOrReadOnly for write access)

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # must be logged in to view

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # all CRUD ops require login
