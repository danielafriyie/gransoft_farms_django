from django import forms
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404

from .models import FinanceModel, ItemDetail


def base_formset(parent_model, child_model, extra=1, **kwargs):
    return inlineformset_factory(
        parent_model, child_model,
        fields=('quantity', 'unit_price', 'amount', 'description'),
        widgets={
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'quantity'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'unit price'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control form-amount', 'placeholder': 'amount'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'description'}),
        }, extra=extra, **kwargs
    )


CreateFinanceItemDetailFormSet = base_formset(FinanceModel, ItemDetail)
UpdateFinanceItemDetailFormSet = base_formset(FinanceModel, ItemDetail)


class BaseFinanceForm(forms.ModelForm):
    class Meta:
        model = FinanceModel
        fields = (
            'supplier_name', 'phone', 'address', 'invoice_no', 'auth_user', 'category'
        )
        widgets = {
            'supplier_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'invoice_no': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }

    @property
    def form_data(self):
        return {
            'supplier_name': self.cleaned_data['supplier_name'],
            'phone': self.cleaned_data['phone'],
            'address': self.cleaned_data['address'],
            'category': self.cleaned_data['category']
        }


class CreateFinanceForm(BaseFinanceForm):
    pass


class UpdateFinanceForm(BaseFinanceForm):
    class Meta(BaseFinanceForm.Meta):
        fields = (
            'supplier_name', 'phone', 'address', 'category'
        )

    def save(self, user, pk, inv_no):
        finance_instance = get_object_or_404(FinanceModel, pk=pk, invoice_no=inv_no)
        finance_instance.supplier_name = self.form_data['supplier_name']
        finance_instance.phone = self.form_data['phone']
        finance_instance.address = self.form_data['address']
        finance_instance.category = self.form_data['category']
        finance_instance.auth_user = user
        finance_instance.save()
        return finance_instance
