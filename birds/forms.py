from django import forms
from .models import PenHouse


class PenHouseForm(forms.ModelForm):
    class Meta:
        model = PenHouse
        widgets = {
            'pen_number': forms.TextInput(attrs={'class': 'form-control'}),
            'pen_name': forms.TextInput(attrs={'class': 'form-control'}),
            'auth_user': forms.TextInput(attrs={'class': 'form-control'}),
        }
        fields = ('pen_number', 'pen_name', 'auth_user')
