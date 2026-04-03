from django import forms

from sights.models import Sight, Category


class SightForm(forms.ModelForm):
    class Meta:
        model = Sight
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'