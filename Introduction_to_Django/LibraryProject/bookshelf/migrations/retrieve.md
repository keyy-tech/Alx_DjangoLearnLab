# RETRIEVE
book = Book.objects.get(title="1984")
book.id, book.title, book.author, book.publication_year
# (1, '1984', 'George Orwell', 1949)