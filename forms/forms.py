from django import forms
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone

from main.models import Book, Genre, Rent, BookCopy, Return, Client


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class BookAddForm(forms.ModelForm):
    copies_count = forms.IntegerField(min_value=1, label = 'Количество экземпляров')
    addit_imgs = MultipleFileField(required=False)
    class Meta:
        model = Book
        fields = '__all__'


# class ClientRegistrationForm(forms.ModelForm):
#     class Meta:
#         model = Client
#         fields = '__all__'

class ClientRegistrationForm(forms.ModelForm):

    class Meta:
        model = Client

        fields = [
            'first_name',
            'last_name',
            'middle_name',
            'email',
            'birth_date',
        ]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150, widget = forms.PasswordInput)




class ChangeCredentionalForm(forms.Form):
    username = forms.CharField(max_length=150, required=False)
    password = forms.CharField(max_length=150, widget = forms.PasswordInput, required=False)


class RedaktorBookForm(forms.ModelForm):
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = Book
        fields = '__all__'


class RedaktorBookImagesForm (forms.Form):
    img = forms.ImageField()
    id = forms.IntegerField(widget = forms.HiddenInput(),required=False)

BookImagesForm = forms.formset_factory(RedaktorBookImagesForm, can_delete=True)






class RentForm(forms.ModelForm):
    books = forms.ModelMultipleChoiceField(
        queryset=BookCopy.objects.filter(status='available'),
        widget=forms.CheckboxSelectMultiple,
        label="Выберите книги"
    )

    class Meta:
        model = Rent
        fields = ['client']
        # fields = ['client', 'planned_return_date']

        def __str__(self):
            return f"{self.book.title} (экз. #{self.id})"





class ReturnForm(forms.Form):
    rental = forms.ModelChoiceField(
        queryset=Rent.objects.filter(return_status=False),
        empty_label="--------- Выберите выдачу ---------",
        label="Выберите выдачу"
    )

    # Добавляем поле даты с автоподстановкой сегодняшнего дня
    return_date = forms.DateField(
        initial=timezone.now,
        label="Дата возврата",
        widget=forms.DateInput(attrs={'type': 'date'})  # Сделает удобный календарь в браузере
    )


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['rental'].widget.attrs.update({
            'id': 'id_rental',
            'onchange': 'this.form.submit();'
        })

        self.fields['rental'].label_from_instance = (
            lambda obj:
            f"{obj.client.last_name} "
            f"{obj.client.first_name} "
            f"(выдача #{obj.id})"
        )