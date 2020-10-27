from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib import messages as msg

from datetime import datetime as dt

from mixins import PermissionRequiredMixin, DeleteModelObjectMixin, ModuleAccesRedirectMixin, ManageModuleViewMixin
from .forms import (
    CreatePurchaseForm, UpdatePurchaseForm, CreatePurchaseDetailFormSet, UpdatePurchaseDetailFormSet
)
from .models import PurchaseModel, PurchaseDetail


class MainModuleMixin(ModuleAccesRedirectMixin, View):
    perm_link = (
        ('finance:create_purchase', 'finance.finance_pur_add_new'),
        ('finance:manage_purchases', 'finance.finance_pur_update'),
    )


###############################################
#       PURCHASES
#############################################
class CreatePurchase(PermissionRequiredMixin, View):
    perm = 'finance.finance_pur_add_new'

    def get(self, request):
        return render(request, 'finance/purchases/create_purchase.html', {
            'form': CreatePurchaseForm(initial={'auth_user': self.request.user}),
            'purchase_detail_form': CreatePurchaseDetailFormSet(queryset=PurchaseDetail.objects.none()),
        })

    def post(self, request):
        form = CreatePurchaseForm(request.POST)
        purchase_detail_form = CreatePurchaseDetailFormSet(data=request.POST)
        if form.is_valid() and purchase_detail_form.is_valid():
            purchase_detail_form.instance = form.save()
            purchase_detail_form.save()
            msg.success(request, 'Purchase created successfully!')
            return redirect('finance:create_purchase')
        msg.error(request, 'There\'s an error in your form!')
        return render(request, 'finance/purchases/create_purchase.html', {
            'form': form,
            'purchase_detail_form': purchase_detail_form
        })


class UpdatePurchase(PermissionRequiredMixin, View):
    perms = 'finance.finance_pur_update'
    template = 'finance/purchases/update_purchase.html'

    def get(self, request):
        purchase = get_object_or_404(PurchaseModel, invoice_no=request.GET['inv_no'])
        form = UpdatePurchaseForm(instance=purchase)
        purchase_detail_form = UpdatePurchaseDetailFormSet(instance=purchase)
        return render(request, 'finance/purchases/update_purchase.html', {
            'form': form,
            'purchase_detail_form': purchase_detail_form,
        })

    def post(self, request):
        purchase = get_object_or_404(PurchaseModel, invoice_no=request.POST['inv_no'], pk=request.POST['p_id'])
        form, prev_path = UpdatePurchaseForm(request.POST), request.POST['prev-path']
        purchase_detail_form = UpdatePurchaseDetailFormSet(data=request.POST, instance=purchase)
        if form.is_valid() and purchase_detail_form.is_valid():
            form.save(request.user, request.POST['p_id'], request.POST['inv_no'])
            purchase_detail_form.save()
            msg.success(request, 'Purchase updated successfully!')
            return redirect(prev_path) if prev_path else redirect('finance:manage_purchases')
        msg.error(request, 'There\'s an error in your form!')
        return render(request, self.template, {
            'form': form,
            'purchase_detail_form': purchase_detail_form,
        })


class ManagePurchases(PermissionRequiredMixin, ManageModuleViewMixin, View):
    perm = 'finance.finance_pur_update'
    template = 'finance/purchases/manage_purchases.html'
    model = PurchaseModel
    values_list_cols = ('id', 'supplier_name', 'phone', 'address', 'invoice_no', 'date_created')
    order_col = '-date_created'

    def purchase_data(self, **filters):
        return super().query_set.filter(**filters, is_default=False)

    @property
    def query_set(self):
        cd = dt.now().date()  # current date
        qs = self.purchase_data(date_created__gte=cd, date_created__lte=cd)

        if ('date1' and 'date2') in self.request.GET and all([self.request.GET['date1'], self.request.GET['date2']]):
            qs = self.purchase_data(
                date_created__gte=self.request.GET['date1'], date_created__lte=self.request.GET['date2']
            )

        if 'search' in self.request.GET and self.request.GET['search']:
            search = self.request.GET['search']
            qs = self.purchase_data(invoice_no__icontains=search)
            if not qs:
                qs = self.purchase_data(supplier_name__icontains=search)
        return qs

    @property
    def get_context(self):
        query_path = None
        if ('date1' or 'date2' or 'search') in self.request.GET:
            import re
            query_path = self.request.get_full_path()
            exclude_url_kwargs = re.compile(self.exclude_url_kwargs_pattern).findall(query_path)
            if exclude_url_kwargs:
                for url_kwarg in exclude_url_kwargs:
                    query_path = query_path.strip(url_kwarg)

        super().get_context.pop('query_path')
        super().get_context['query_path'] = query_path

        return super().get_context


class DeletePurchase(PermissionRequiredMixin, DeleteModelObjectMixin, View):
    perm = 'finance.finance_pur_delete'
    model = PurchaseModel
    values_list = 'invoice_no'

    @property
    def get_success_url(self):
        return self.request.POST['path']
