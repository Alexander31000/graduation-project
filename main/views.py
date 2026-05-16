from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from forms.forms import RedaktorBookForm, RedaktorBookImagesForm, BookImagesForm
from main.models import Book, BookImages, Genre, Client


# Create your views here.


def get_main_page(request):

    books = Book.objects.all()
    genres = Genre.objects.all()
    # imgs = Book.objects.filter('img')
    # Показывать по 10 книг на странице
    paginator = Paginator(books, 10)

    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)

    context = {'books': books,
               'genres': genres,
               # 'imgs': imgs,
               }

    return render(request, 'main.html', context)



def client_list(request):

    sort = request.GET.get('sort', 'last_name').strip()
    clients = Client.objects.all().order_by(sort)
    paginator = Paginator(clients, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'current_sort': sort
    }

    return render(
        request,
        'ClientList.html',
        context
    )


def genre_filter(request, id):
    all_genres = Genre.objects.all()
    genres = Genre.objects.filter(id=id)
    books = Book.objects.filter(genres=id)
    context = {'genres': all_genres,
               'books': books,
               'selected_genre': genres,
               }

    return render(request, 'main.html', context)


def book_detail(request, id):
    book = Book.objects.get(id=id)

    additional_imgs = BookImages.objects.filter(book_id=id).select_related('book')

    context = {'book': book,
               'additional_imgs': additional_imgs, }

    return render(request, 'book_detail.html', context)


def redaktor_page(request, id):
    book = get_object_or_404(Book, id=id)
    addit_imgs = BookImages.objects.filter(
        book=book)  # найти все записи модели BookImages где поле book равно объекту book

    initial_imgs = [{'img': i.addit_imgs, 'id': i.id} for i in addit_imgs]
    # di = {
    #     "title": book.title,
    #     "description": book.description,
    #     "author": book.author,
    #     "daily_price": book.daily_price,
    #     "status": book.status,
    #     "img": book.img,
    # }
    # form = RedaktorBookForm(initial=di)
    form_set = BookImagesForm(initial=initial_imgs)
    if request.method == "POST":
        form = RedaktorBookForm(request.POST, request.FILES, instance=book)
        form_set = BookImagesForm(request.POST, request.FILES, initial=initial_imgs)
        if form.is_valid() and form_set.is_valid():
            form.save()
            for form_img in form_set:
                if form_img in form_set.deleted_forms:
                    continue
                if form_img.has_changed():
                    new_file = form_img.cleaned_data.get('img')
                    img_id = form_img.cleaned_data.get('id')
                    if img_id: # Если картинка уже была в базе - обновляем
                        instance = BookImages.objects.get(id=img_id)
                        if new_file:
                            instance.addit_imgs = new_file
                            instance.save()
                        elif new_file: # Если это новое поле и в него загрузили файл
                            BookImages.objects.create(addit_imgs=new_file, book=book)

            # Массовое удаление помеченных картинок
        delete_ids = [f.cleaned_data.get('id') for f in form_set.deleted_forms if f.cleaned_data.get('id')]
        BookImages.objects.filter(id__in=delete_ids).delete()

        return redirect('book_detail', book.id)
    else:
        form = RedaktorBookForm(instance=book)
        form_set = BookImagesForm(initial=initial_imgs)



    context = {
        'book': book,
        'form': form,
        'form_set': form_set,
        'additional_imgs': addit_imgs,
    }
    return render(request, 'book_redaktor.html', context)
