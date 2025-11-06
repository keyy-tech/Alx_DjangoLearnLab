from relationship_app.models import Author, Library, Librarian, Book

Book.objects.select_related("author")


library = Library.objects.prefetch_related('books').get(name="library_name")
books = library.books.all()
