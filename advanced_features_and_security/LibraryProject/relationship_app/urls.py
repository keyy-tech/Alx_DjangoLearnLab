from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='list_books'),           # used by register/login redirects
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
    path('books/', views.book_list, name='book_list'),
    path('books/create/', views.create_book, name='create_book'),
    path('books/<int:book_id>/edit/', views.update_book, name='update_book'),
    path('books/<int:book_id>/delete/', views.delete_view, name='delete_view'),
]

