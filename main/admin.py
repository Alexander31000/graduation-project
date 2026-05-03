from django.contrib import admin

from main.models import Book, Rent, BookImages, Client, Genre, BookCopy


# Register your models here.


class BookCopyInline(admin.TabularInline):
    model = BookCopy
    extra = 0  # сколько пустых форм показывать
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'daily_price', 'total_copies', 'available_copies')
    list_display_links = ('title', 'status')
    search_fields = ('title', 'status')
    inlines = [BookCopyInline]

admin.site.register(Book, BookAdmin)  # Функция admin.site.register принимает либо одну модель и её класс настроек, либо список моделей (но тогда без настроек).
admin.site.register(Client)
admin.site.register(Rent)
admin.site.register(BookImages)
admin.site.register(Genre)
admin.site.register(BookCopy)
# admin.site.register(RentBookItem)
# admin.site.register(Return)
# admin.site.register(ReturnBookItem)







