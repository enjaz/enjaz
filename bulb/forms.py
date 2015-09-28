from django import forms

from bulb.models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'authors', 'edition',
                  'condition', 'description', 'cover',
                  'category']
