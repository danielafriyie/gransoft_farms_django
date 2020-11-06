from django import forms
from django.shortcuts import get_object_or_404
from .models import PenHouse, BirdsStock, MortalityCull, MedicineFeed
from finance.models import FinanceModel


class PenHouseForm(forms.ModelForm):
    class Meta:
        model = PenHouse
        widgets = {
            'pen_number': forms.TextInput(attrs={'class': 'form-control'}),
            'pen_name': forms.TextInput(attrs={'class': 'form-control'}),
            'auth_user': forms.HiddenInput(attrs={'class': 'form-control'}),
        }
        fields = ('pen_number', 'pen_name', 'auth_user')


class BirdsStockForm(forms.ModelForm):
    invoice_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)

    class Meta:
        model = BirdsStock
        widgets = {
            'pen_house': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'auth_user': forms.HiddenInput(attrs={'class': 'form-control'}),
        }
        fields = ('pen_house', 'auth_user', 'quantity')

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.invoice_no = get_object_or_404(FinanceModel, invoice_no=self.cleaned_data['invoice_no'])
        return super().save(commit=commit)


class MortCullForm(forms.ModelForm):
    class Meta:
        model = MortalityCull
        fields = ('pen_house', 'auth_user', 'category', 'quantity', 'description')
        widgets = {
            'pen_house': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'auth_user': forms.HiddenInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'})
        }


class MedFeedForm(forms.ModelForm):
    class Meta:
        model = MedicineFeed
        fields = ('pen_house', 'auth_user', 'category', 'quantity', 'description')
        widgets = {
            'pen_house': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control'}),
            'auth_user': forms.HiddenInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'})
        }
