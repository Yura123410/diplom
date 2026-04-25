from django import forms
from reviews.models import Review


class ReviewForm(forms.ModelForm):
    title = forms.CharField(
        max_length=150,
        label='Заголовок',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        label='Текст отзыва'
    )

    rating = forms.IntegerField(
        label='Оценка',
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1,
            'max': 5,
            'step': 1,
            'style': 'width: 100px;'
        }),
        initial=5,
        help_text='Оцените от 1 до 5'
    )

    slug = forms.SlugField(
        max_length=20,
        initial='temp_slug',
        widget=forms.HiddenInput(),
        required=False
    )

    class Meta:
        model = Review
        fields = ('sight', 'title', 'content', 'rating', 'slug')
        widgets = {
            'sight': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'sight': 'Достопримечательность',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Делаем поле только для чтения, но отправляемым
            self.fields['sight'].widget.attrs['readonly'] = 'readonly'
            self.fields['sight'].required = False
            # Убираем disabled если был
            if 'disabled' in self.fields['sight'].widget.attrs:
                del self.fields['sight'].widget.attrs['disabled']
