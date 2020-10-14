from django import forms
from django.shortcuts import get_object_or_404

from .models import PurchasesModel


class BasePurchaseForm(forms.ModelForm):
    class Meta:
        model = PurchasesModel
        fields = (
            'supplier_name', 'phone', 'address', 'quantity', 'unit_price', 'amount', 'description', 'invoice_no',
            'auth_user'
        )
        widgets = {
            'supplier_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'invoice_no': forms.TextInput(attrs={'class': 'form-control'}),
        }

    @property
    def form_data(self):
        return {
            # 'id': self.cleaned_data['id'],
            'supplier_name': self.cleaned_data['supplier_name'],
            'phone': self.cleaned_data['phone'],
            'address': self.cleaned_data['address'],
            'quantity': self.cleaned_data['quantity'],
            'unit_price': self.cleaned_data['unit_price'],
            'amount': self.cleaned_data['amount'],
            'description': self.cleaned_data['description'],
        }


class CreatePurchaseForm(BasePurchaseForm):
    pass


class UpdatePurchaseForm(BasePurchaseForm):
    class Meta(BasePurchaseForm.Meta):
        fields = (
            'supplier_name', 'phone', 'address', 'quantity', 'unit_price', 'amount', 'description'
        )

    def save(self, user, pk, inv_no):
        purchase = get_object_or_404(PurchasesModel, pk=pk, invoice_no=inv_no)
        purchase.supplier_name = self.form_data['supplier_name']
        purchase.phone = self.form_data['phone']
        purchase.address = self.form_data['address']
        purchase.quantity = self.form_data['quantity']
        purchase.unit_price = self.form_data['unit_price']
        purchase.amount = self.form_data['amount']
        purchase.description = self.form_data['description']
        purchase.auth_user = user
        purchase.save()
