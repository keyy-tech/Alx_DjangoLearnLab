from relationship_app.models import Author, Library, Librarian, Book

Book.objects.select_related("author")
