from django import forms
from django.contrib.auth.password_validation import validate_password

from main.models import Book, Genre, Rent, BookCopy, Return


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
    addit_imgs = MultipleFileField(required=False)
    class Meta:
        model = Book
        fields = '__all__'


# class ClientRegistrationForm(forms.ModelForm):
#     class Meta:
#         model = Client
#         fields = '__all__'

class ClientRegistrationForm(forms.Form):

    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150, validators=[validate_password], widget = forms.PasswordInput)
    password_protect = forms.CharField(max_length=150, widget = forms.PasswordInput)
    register_date = forms.DateField(required=False)

    def clean(self):
            cleaned_data = super().clean()
            if cleaned_data.get('password') != cleaned_data.get('password_protect'):
                self.add_error('password_protect', 'Пароли не совпадают')



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





class ReturnForm(forms.Form):
    rental = forms.ModelChoiceField(
        queryset=Rent.objects.filter(return_status=False),
        label="Выберите выдачу"
    )
    class Meta:
        model = Return
        fields = '__all__'