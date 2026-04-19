from django import forms

from reviews.models import Review


class ReviewForm(forms.ModelForm):
    title = forms.CharField(max_length=150, label='Заголовок')
    content = forms.TextInput
    slug = forms.SlugField(max_length=20, initial='temp_slug', widget=forms.HiddenInput())

    class Meta:
        model = Review
        fields = ('sight', 'title', 'content', 'slug')
