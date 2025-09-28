from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Author, Book


class BookAPITests(APITestCase):
    """
    Test suite for Book API endpoints:
    - CRUD operations
    - Filtering, searching, ordering
    - Permissions & authentication
    """

    def setUp(self):
        # Create user for authenticated tests
        self.user = User.objects.create_user(username="testuser", password="testpass123")

        # Create authors and books
        self.author1 = Author.objects.create(name="George Orwell")
        self.author2 = Author.objects.create(name="Aldous Huxley")

        self.book1 = Book.objects.create(title="1984", publication_year=1949, author=self.author1)
        self.book2 = Book.objects.create(title="Animal Farm", publication_year=1945, author=self.author1)
        self.book3 = Book.objects.create(title="Brave New World", publication_year=1932, author=self.author2)

        # APIClient for requests
        self.client = APIClient()

    # ------------------------
    # CRUD TESTS
    # ------------------------

    def test_list_books(self):
        """Anyone can view the list of books."""
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_retrieve_book(self):
        """Anyone can view a single book."""
        url = reverse('book-detail', args=[self.book1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "1984")

    def test_create_book_authenticated(self):
        """Authenticated users can create books."""
        self.client.login(username="testuser", password="testpass123")
        url = reverse('book-create')
        data = {"title": "New Book", "publication_year": 2020, "author": self.author1.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)

    def test_create_book_unauthenticated(self):
        """Unauthenticated users cannot create books."""
        url = reverse('book-create')
        data = {"title": "New Book", "publication_year": 2020, "author": self.author1.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_authenticated(self):
        """Authenticated users can update books."""
        self.client.login(username="testuser", password="testpass123")
        url = reverse('book-update', args=[self.book1.id])
        data = {"title": "Updated 1984", "publication_year": 1949, "author": self.author1.id}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated 1984")

    def test_delete_book_authenticated(self):
        """Authenticated users can delete books."""
        self.client.login(username="testuser", password="testpass123")
        url = reverse('book-delete', args=[self.book1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    def test_delete_book_unauthenticated(self):
        """Unauthenticated users cannot delete books."""
        url = reverse('book-delete', args=[self.book2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ------------------------
    # FILTER / SEARCH / ORDER
    # ------------------------

    def test_filter_books_by_year(self):
        url = reverse('book-list') + '?publication_year=1949'
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "1984")

    def test_search_books_by_title(self):
        url = reverse('book-list') + '?search=Farm'
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Animal Farm")

    def test_order_books_by_year_desc(self):
        url = reverse('book-list') + '?ordering=-publication_year'
        response = self.client.get(url)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
