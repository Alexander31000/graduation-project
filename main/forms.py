import forms
from main.models import Book, Client


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


class BookModelForm(forms.ModelForm):
    additional_image = MultipleFileField(required=False)
    class Meta:
        model = Book
        fields = '__all__'



class ClientModelForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
