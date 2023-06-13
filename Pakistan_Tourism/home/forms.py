from django import forms
from .models import Review_Rating,Tour_Reviews
class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review_Rating
        fields=['review','rating']

class TourForm(forms.ModelForm):
    class Meta:
        model=Tour_Reviews
        fields=['review','rating']


