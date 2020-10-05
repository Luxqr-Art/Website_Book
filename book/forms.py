from django import forms

from .models import Reviews, Rating, RatingStar

class ReviewForm(forms.ModelForm):
    """Форма отзыва"""
    class Meta:
        model = Reviews
        fields = ['title', 'email', 'text']

class RatingForm(forms.ModelForm):
    """
    Форма добавление рейтинга
    """
    class Meta:
        model = Rating
        fields = ('star',)
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None

    )
