from datetime import date, timedelta
from django.utils import timezone
from django.contrib import messages


from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from forms.forms import ClientRegistrationForm, BookAddForm, LoginForm, ChangeCredentionalForm, RentForm, ReturnForm
from main.models import BookImages, Book, Client, Rent, RentBookItem, Return, ReturnItem, BookCopy
from main.views import get_main_page


# Create your views here.


# class BookCreateView(CreateView):
#     template_name = 'BookAddForm.html'
#     form_class = BookAdd
#     success_url = reverse_lazy('main_page')
#
#     def form_valid(self, form):
#         response = super().form_valid(form)
#
#         images = self.request.FILES.getlist('images')
#
#         for img in images:
#             BookImage.objects.create(
#                 book=self.object,
#                 img=img
#             )
#
#         return response
#
#
# class ClientCreateView(CreateView):
#     template_name = 'ClientRegistration.html'
#     form_class = ClientAdd
#     success_url = reverse_lazy(get_main_page)

def book_create_form(request):
    book_add_form = BookAddForm()
    if request.method == 'POST':
        book_add_form = BookAddForm(request.POST, request.FILES)
        if book_add_form.is_valid():
            new_book = Book(
                title=book_add_form.cleaned_data['title'],
                author=book_add_form.cleaned_data['author'],
                daily_price=book_add_form.cleaned_data['daily_price'],
                img=book_add_form.cleaned_data['img'],
                description=book_add_form.cleaned_data['description'],
            )
            new_book.save()
            copies_count = book_add_form.cleaned_data['copies_count']

            for bok in range(copies_count):
                BookCopy.objects.create(
                    book=new_book,
                    status='available'
                )
            new_book.genres.set(book_add_form.cleaned_data['genres'])


            addit_imgs = book_add_form.cleaned_data['addit_imgs']
            if addit_imgs:
                for img in addit_imgs:
                    addit_imgs = BookImages(
                        addit_imgs=img,
                        book=new_book
                    )
                    addit_imgs.save()
            else:
                return redirect('main_page')
        return redirect('main_page')
    form = book_add_form

    context = {
        'form': form,
    }

    return render(request, 'BookAddForm.html', context)


def client_reg_form(request):
    form = ClientRegistrationForm()
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Читатель успешно зарегистрирован'
            )

            return redirect('main_page')

        return render(
            request,
            'ClientRegistration.html',
            {'form': form}
        )
    #         user = User(username=form.cleaned_data['username'])
    #         password = form.cleaned_data['password']
    #         if User.objects.filter(username=form.cleaned_data['username']):
    #             form.add_error('username', 'Username already registered')
    #         else:
    #             user.set_password(password)
    #             user.save()
    #             Client.objects.create(user=user, register_date=date.today())
    #             return redirect('main_page')
    #
    context = {
        'form': form,
    }

    return render(request, 'ClientRegistration.html', context)


def login_form(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request,
                                username=username,
                                password=password
                                )

            if user is not None:
                login(request, user)
                return redirect('main_page')
            else:
                form.add_error(None, 'Неверный логин или пароль')

    context = {
        'form': form,
    }
    return render(request, 'login.html', context)


def log_out(request):
    logout(request)
    return redirect('main_page')


# def redactor_user(request)\
#     # по ТЗ уже лишнее
#     user = request.user
#     form = ChangeCredentionalForm(initial={"username": user.username,
#                                            "password": user.password, })
#
#     if request.method == 'POST':
#         form = ChangeCredentionalForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             if username != user.username:
#                 user.username = username
#             if password != user.password:
#                 user.set_password(password)
#             user.save()
#             return redirect('main_page')
#
#
#
#
#     context = {
#         'form': form
#     }
#
#     return render(request, 'redactor_user.html', context)



# def create_rent(request):
#     form = RentForm()
#     if request.method == 'POST':
#         form = RentForm(request.POST)
#
#         if form.is_valid():
#             rent = form.save()
#             rent.start_date = timezone.now()
#
#
#             books = form.cleaned_data['books']
#
#
#             # 🚨 проверка количества
#             if len(books) > 5:
#                 form.add_error('books', 'Максимум 5 книг')
#                 return render(request, 'RentForm.html', {'form': form})
#
#
#             total_price = 0
#
#             for book in books:
#                 # создаём запись
#                 RentBookItem.objects.create(
#                     rental=rent,
#                     book_copy=book,
#                     price_per_day=book.book.daily_price
#                 )
#
#                 # меняем статус
#                 book.status = 'rented'
#                 book.save()
#
#                 total_price += book.book.daily_price * 30
#
#             # 💰 скидки
#             if len(books) > 4:
#                 total_price *= 0.85
#             elif len(books) > 2:
#                 total_price *= 0.90
#
#             rent.total_price = total_price
#             rent.save()
#
#             return redirect('main_page')
#
#     else:
#         form = RentForm()
#
#
#     context = {'form': form}
#
#     return render(request, 'RentForm.html', context)

def create_rent(request):
    if request.method == 'POST':
        form = RentForm(request.POST)

        if form.is_valid():

            client = form.cleaned_data['client']
            books = form.cleaned_data['books']
            book_ids = []

            for copy in books:

                if copy.book.id in book_ids:
                    form.add_error(
                        'books',
                        f'Нельзя выдавать несколько экземпляров книги "{copy.book.title}"'
                    )

                    return render(
                        request,
                        'RentForm.html',
                        {'form': form}
                    )

                book_ids.append(copy.book.id)

            active_rents = Rent.objects.filter(client=client, return_status=False)

            if active_rents.exists():
                form.add_error(
                    'client',
                    'У читателя есть невозвращенные книги'
                )

                return render(request, 'RentForm.html',{'form': form})

            rent = form.save(commit=False)
            count = len(books)

            if count > 5:
                form.add_error('books', 'Более 5 книг выдавать запрещено.')
                return render(request, 'RentForm.html', {'form': form})

            rent.save()

            total_sum = 0
            book_titles = []

            for book_copy in books:
                # Берем цену напрямую из модели Book
                book_price = book_copy.book.daily_price

                RentBookItem.objects.create(
                    rental=rent,
                    book_copy=book_copy,
                    price_per_day=book_price
                )

                book_copy.status = 'rented'
                book_copy.save()

                # Просто суммируем цены книг
                total_sum += book_price * 30
                book_titles.append(book_copy.book.title)

            # Применяем скидку к общей сумме
            if count > 4:
                total_sum *= 0.85  # -15%
            elif count > 2:
                total_sum *= 0.90  # -10%

            rent.total_price = total_sum
            rent.planned_return_date = timezone.now().date() + timedelta(days=30)
            rent.save()

            books_str = ", ".join(book_titles)
            messages.success(request,f""" Выдача оформлена. Книги:{books_str} Сумма: {rent.total_price} р. Вернуть до:{rent.planned_return_date}""")

            return render(request, 'RentForm.html', {'form': form})
    else:
        form = RentForm()
    return render(request, 'RentForm.html', {'form': form})






def return_books(request):
    form = ReturnForm()
    if request.method == 'POST':
        rental_id = request.POST.get('rental')
        rental = get_object_or_404(Rent, id=rental_id)

        if Return.objects.filter(rental=rental).exists():
            return redirect('main_page')

        today = timezone.now().date()
        delay_days = (today - rental.planned_return_date).days
        delay_penalty = 0
        if delay_days > 0:
            # Штраф 1% в день от суммы аренды за просрочку
            delay_penalty = rental.total_price * 0.01 * delay_days

        return_act = Return.objects.create(rental=rental, penalty=delay_penalty,total_price=rental.total_price + delay_penalty)
        # возврат
        total_damage_penalty = 0
        for item in rental.items.all():
            copy = item.book_copy
            dmg_text = request.POST.get(f'damage_{copy.id}', '')
            current_item_pen = 50 if dmg_text else 0
            total_damage_penalty += current_item_pen
            rating = request.POST.get(f'rating_{copy.id}')

            ReturnItem.objects.create(
                return_act=return_act,
                book_copy=copy,
                damage=dmg_text,
                pen=current_item_pen,
                rating=rating
            )

            # Освобождаем книгу
            copy.status = 'available'
            copy.save()

            # Финализируем Rent и Return
        rental.return_status = True
        rental.save()

        return_act.penalty += total_damage_penalty
        return_act.total_price += total_damage_penalty
        return_act.save()

        messages.success(request, f"Книга: {return_act.total_price} успешна возвращена.)")
        messages.success(request, f"Успешно. К оплате: {return_act.total_price} р. (Штраф: {return_act.penalty} р.)")
        return redirect('return_books')

    else:
        form = ReturnForm()

    context = {'form': form,
               'message': messages.success}

    return render(request, 'ReturnForm.html', context)


