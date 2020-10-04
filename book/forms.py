from django import forms

from .models import Reviews

class ReviewForm(forms.ModelForm):
    """Форма отзыва"""
    class Meta:
        model = Reviews
        fields = ['title', 'email', 'text']
