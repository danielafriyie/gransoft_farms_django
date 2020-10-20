from django import forms
from django.forms import modelformset_factory, BaseModelFormSet, inlineformset_factory
from django.shortcuts import get_object_or_404

from .models import PurchaseModel, PurchaseDetail


class BasePurchaseDetailFormSet(BaseModelFormSet):

    def save(self, commit=True):
        invoice_no = get_object_or_404(PurchaseModel, invoice_no=self.data['invoice_no'])
        for data in self.cleaned_data:
            PurchaseDetail.objects.create(
                invoice_no=invoice_no,
                quantity=data['quantity'],
                unit_price=data['unit_price'],
                amount=data['amount'],
                description=data['description']
            )

    def save_update(self):
        if self.is_valid():
            for data in self.cleaned_data:
                print(data)
                print()
        else:
            print('is not valid')


def base_purchase_detail_formset(extra=1, **kwargs):
    return modelformset_factory(
        PurchaseDetail, fields=('quantity', 'unit_price', 'amount', 'description'),
        widgets={
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'quantity'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'unit price'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'amount'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'description'}),
            'invoice_no': forms.TextInput(attrs={'class': 'form-control'}),
        },
        formset=BasePurchaseDetailFormSet, extra=extra, **kwargs
    )


CreatePurchaseDetailFormSet = inlineformset_factory(
    PurchaseModel, PurchaseDetail,
    fields=('quantity', 'unit_price', 'amount', 'description'),
    widgets={
        'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'quantity'}),
        'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'unit price'}),
        'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'amount'}),
        'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'description'}),
    }, extra=1
)
UpdatePurchaseDetailFormSet = inlineformset_factory(
    PurchaseModel, PurchaseDetail,
    fields=('quantity', 'unit_price', 'amount', 'description'),
    widgets={
        'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'quantity'}),
        'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'unit price'}),
        'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'amount'}),
        'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'description'}),
    }, extra=1
)


class BasePurchaseForm(forms.ModelForm):
    class Meta:
        model = PurchaseModel
        fields = (
            'supplier_name', 'phone', 'address', 'invoice_no', 'auth_user'
        )
        widgets = {
            'supplier_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'invoice_no': forms.TextInput(attrs={'class': 'form-control'}),
        }

    @property
    def form_data(self):
        return {
            'supplier_name': self.cleaned_data['supplier_name'],
            'phone': self.cleaned_data['phone'],
            'address': self.cleaned_data['address'],
        }


class CreatePurchaseForm(BasePurchaseForm):
    pass


class UpdatePurchaseForm(BasePurchaseForm):
    class Meta(BasePurchaseForm.Meta):
        fields = (
            'supplier_name', 'phone', 'address',
        )

    def save(self, user, pk, inv_no):
        purchase = get_object_or_404(PurchaseModel, pk=pk, invoice_no=inv_no)
        purchase.supplier_name = self.form_data['supplier_name']
        purchase.phone = self.form_data['phone']
        purchase.address = self.form_data['address']
        purchase.auth_user = user
        purchase.save()
        return purchase
