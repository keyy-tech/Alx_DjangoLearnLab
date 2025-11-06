from relationship_app.models import Author, Library, Librarian, Book

Book.objects.select_related("author")


library = Library.objects.prefetch_related("books").get(name="library_name")
books = library.books.all()


from relationship_app.models import Library


def list_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    books = library.books.all()
    return books



def query_books_by_a_specific_author(author_name):
    author = Author.objects.get(name=author_name)
    book_author = Book.objects.filter(author=author)
    return book_author
