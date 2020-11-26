from django import forms
from .models import EggsModel


class EggsForm(forms.ModelForm):
    class Meta:
        model = EggsModel
        widgets = {
            'pen': forms.Select(attrs={'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'auth_user': forms.HiddenInput(attrs={'class': 'form-control'}),
        }
        fields = ('pen', 'time', 'quantity', 'auth_user')
