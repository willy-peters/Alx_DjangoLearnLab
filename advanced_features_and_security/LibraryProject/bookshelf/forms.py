# bookshelf/forms.py
from django import forms
from .models import Book


class ExampleForm(forms.Form):
    """
    Example form used in form_example.html to demonstrate CSRF protection
    and safe user input handling.
    """
    title = forms.CharField(max_length=100, required=True)
    author = forms.CharField(max_length=100, required=True)


class BookSearchForm(forms.Form):
    q = forms.CharField(required=False, max_length=200)

    def clean_q(self):
        q = self.cleaned_data.get("q", "")
        q = q.strip()
        return q


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "published_date"]
