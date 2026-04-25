from django import forms
from sights.models import Sight, Category, SightPhoto


class SightForm(forms.ModelForm):
    class Meta:
        model = Sight
        exclude = ('views_count', 'latitude', 'longitude')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'full_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'opening_hours': forms.TextInput(attrs={'class': 'form-control'}),
            'ticket_price': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Название',
            'category': 'Категория',
            'short_description': 'Краткое описание',
            'full_description': 'Полное описание',
            'address': 'Адрес',
            'website': 'Официальный сайт',
            'image': 'Главное изображение',
            'opening_hours': 'Часы работы',
            'ticket_price': 'Стоимость билета',
        }
        help_texts = {
            'address': 'Введите полный адрес достопримечательности',
            'website': 'Например: https://example.com (оставьте пустым, если нет сайта)',
            'opening_hours': 'Например: Пн-Вс 10:00-18:00',
            'ticket_price': 'Например: 500 руб. или Бесплатно',
        }


class SightPhotoForm(forms.ModelForm):
    class Meta:
        model = SightPhoto
        fields = ('image',)
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
        labels = {
            'image': 'Фотография',
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'name': 'Название категории',
            'description': 'Описание категории',
        }