from datetime import timedelta
from django.utils import timezone
from email.policy import default

from django.contrib.auth.models import User
from django.db import models

# Create your models here.




class Genre(models.Model):
    genre_choice = [('historical', 'историческое'),
                    ('romance', 'роман'),
                    ('detective', 'детектив'),
                    ('adventure', 'приключения'),
                    ('prose', 'проза'),]
    genre_name = models.CharField(max_length=100, choices=genre_choice)
    def __str__(self):
        return self.genre_name




class Book(models.Model):
    # хранит сущность книги
    status_choice = [('available','доступна'),
                     ('unavailable', 'недоступная')]

    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.CharField(max_length=100)
    daily_price = models.FloatField()
    status = models.CharField(max_length=30, choices=status_choice)
    img = models.ImageField(upload_to='images/')
    genres = models.ManyToManyField(Genre, related_name='books')

    def __str__(self):
        return self.title
    def total_copies(self):
        return self.copies.count()
    def available_copies(self):
        return self.copies.filter(status='available').count()

class BookImages(models.Model):
    # доп картинки у книги
    addit_imgs = models.ImageField(upload_to='book_images', null=False, blank=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)



class BookCopy(models.Model):
    # хранит экземпляры книги
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name='copies')
    status = models.CharField(max_length=100, choices=[
        ('available','доступна'),
        ('rented', 'нет свободных экземпляров'),
        ('unavailable','недоступна'),])

    def __str__(self):
        return self.book.title



class Client(models.Model):
    # клиент
    register_date = models.DateField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name= 'Пользователь', null=False, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Клиенты'
        verbose_name = 'Клиент'
        ordering = ['-register_date']






def default_time():
    return timezone.now() + timedelta(days=30)

class Rent(models.Model):
    client = models.ForeignKey(User, on_delete=models.PROTECT)
    start_date = models.DateField(default=timezone.now)
    planned_return_date = models.DateField(default=default_time)
    total_price = models.FloatField(default=0)
    return_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Выдача #{self.id} - {self.client}"

class RentBookItem(models.Model):
    rental = models.ForeignKey(Rent, on_delete=models.CASCADE, related_name='items')
    book_copy = models.ForeignKey(BookCopy, on_delete=models.PROTECT)
    price_per_day = models.FloatField()


    def __str__(self):
        return f"{self.book_copy} (выдача {self.rental.id})"












class Return(models.Model):
    rental = models.OneToOneField(Rent, on_delete=models.CASCADE)
    return_date = models.DateField(auto_now_add=True)
    penalty = models.FloatField(default=0)
    total_price = models.FloatField(default=0)


    def __str__(self):
        return f"Возврат #{self.id}"


class ReturnItem(models.Model):
    return_act = models.ForeignKey(Return, on_delete=models.CASCADE, related_name='items')
    book_copy = models.ForeignKey(BookCopy, on_delete=models.PROTECT)

    damage = models.TextField(blank=True, null=True)
    pen = models.FloatField(default=0)
    rating = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.book_copy}"


