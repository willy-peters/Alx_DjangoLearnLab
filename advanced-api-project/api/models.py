from django.db import models

class Author(models.Model):
    """
    Represents an author entity who can write multiple books.
    - name: The name of the author.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Represents a book entity linked to an author.
    - title: Title of the book.
    - publication_year: Year the book was published.
    - author: ForeignKey relationship (one author can have many books).
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
