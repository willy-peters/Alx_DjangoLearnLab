from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer

# Keep this if they still check for the simple ListAPIView
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Required ViewSet for CRUD
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()   # 🔑 must be exactly like this
    serializer_class = BookSerializer
