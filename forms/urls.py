from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from forms.views import book_create_form, client_reg_form, login_form, log_out, create_rent, return_books

# urlpatterns = [
#     path('form_book_add', BookCreateView.as_view(), name='book_add'),
#     path('form_client_add', ClientCreateView.as_view(), name='client_add'),
# ]



urlpatterns = [
    path('form_book_add', book_create_form, name='book_add'),
    path('form_client_add', client_reg_form, name='client_add'),
    path('login_page',login_form, name='login'),
    path('log_out', log_out, name='log_out'),
    # path('user_redactor', redactor_user, name='user_redactor'),
    path('create_rent', create_rent, name='create_rent'),
    path('return_books', return_books, name = 'return_books'),

    # path('form_client_add', ClientCreateView.as_view(), name='client_add'),
]