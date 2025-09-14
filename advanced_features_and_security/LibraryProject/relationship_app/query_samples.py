from relationship_app.models import Author, Book, Library, Librarian

def run_queries():
    # Query all books by a specific author using filter
    author_name = "J.K. Rowling"
    try:
        author = Author.objects.get(name=author_name)
        books_by_author = Book.objects.filter(author=author)  # required filter()
        print(f"Books by {author_name}: {[book.title for book in books_by_author]}")
    except Author.DoesNotExist:
        print(f"No author found with name {author_name}")

    # List all books in a library
    library_name = "Central Library"
    try:
        library = Library.objects.get(name=library_name)
        books_in_library = library.books.all()
        print(f"Books in {library_name}: {[book.title for book in books_in_library]}")
    except Library.DoesNotExist:
        print(f"No library found with name {library_name}")

    # Retrieve the librarian for a library using get()
    try:
        librarian = Librarian.objects.get(library=library)  # required get()
        print(f"Librarian for {library_name}: {librarian.name}")
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to {library_name}")
