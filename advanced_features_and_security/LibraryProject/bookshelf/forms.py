# bookshelf/forms.py
from django import forms

class BookSearchForm(forms.Form):
    q = forms.CharField(required=False, max_length=200)

    def clean_q(self):
        q = self.cleaned_data.get("q", "")
        # Additional sanitization if needed; Django will escape on output.
        # Example: strip excessive whitespace and block suspicious input patterns.
        q = q.strip()
        return q

class BookForm(forms.ModelForm):
    class Meta:
        from .models import Book
        model = Book
        fields = ["title", "author", "published_date"]
