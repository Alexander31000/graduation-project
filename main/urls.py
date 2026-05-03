from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from main.views import get_main_page, book_detail, redaktor_page, genre_filter

urlpatterns = [
    path('', get_main_page, name='main_page'),
    path('details/<int:id>/',book_detail, name='book_detail'),
    path('book_redaktor/<int:id>/', redaktor_page, name='book_redaktor'),
    path('genres_books/<int:id>/',genre_filter, name='genre_filter'),
]