from django import forms

from sights.models import Sight


class SightForm(forms.ModelForm):
    class Meta:
        model = Sight
        fields = '__all__'
