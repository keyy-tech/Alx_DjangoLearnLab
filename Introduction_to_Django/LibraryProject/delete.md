book.delete()
Book.objects.all()

# (1, {'bookshelf.Book': 1})  # One book deleted
# <QuerySet []>  # No books remain
