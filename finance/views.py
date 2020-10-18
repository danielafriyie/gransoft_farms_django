from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib import messages as msg
from django.core.paginator import Paginator

from datetime import datetime as dt

from mixins import PermissionRequiredMixin, DeleteModelObjectMixin, ModuleAccesRedirectMixin, ManageModuleViewMixin
from .forms import CreatePurchaseForm, UpdatePurchaseForm
from .models import PurchasesModel


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
        form = CreatePurchaseForm(initial={'auth_user': request.user})
        return render(request, 'finance/purchases/create_purchase.html', {'form': form})

    def post(self, request):
        form = CreatePurchaseForm(request.POST)
        if form.is_valid():
            form.save()
            msg.success(request, 'Purchase created successfully!')
            return redirect('finance:create_purchase')
        msg.error(request, 'There\'s an error in your form!')
        return render(request, 'finance/purchases/create_purchase.html', {'form': form})


class UpdatePurchase(PermissionRequiredMixin, View):
    perms = 'finance.finance_pur_update'

    def get(self, request):
        purchase = get_object_or_404(PurchasesModel, invoice_no=request.GET['inv_no'])
        form = UpdatePurchaseForm(instance=purchase)
        return render(request, 'finance/purchases/update_purchase.html', {'form': form})

    def post(self, request):
        form = UpdatePurchaseForm(request.POST)
        if form.is_valid():
            form.save(request.user, request.POST['p_id'], request.POST['inv_no'])
            msg.success(request, 'Purchase updated successfully!')
            return redirect('finance:manage_purchases')
        msg.error(request, 'There\'s an error in your form!')
        return render(request, 'finance/purchases/update_purchase.html', {'form': form})


class ManagePurchases(PermissionRequiredMixin, ManageModuleViewMixin, View):
    perm = 'finance.finance_pur_update'
    template = 'finance/purchases/manage_purchases.html'
    model = PurchasesModel
    values_list_cols = (
        'id', 'supplier_name', 'phone', 'address', 'invoice_no', 'date_created',
        'quantity', 'unit_price', 'amount'
    )
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

        context = super().get_context
        context.pop('query_path')
        context['query_path'] = query_path

        return context


class DeletePurchase(PermissionRequiredMixin, DeleteModelObjectMixin, View):
    perm = 'finance.finance_pur_delete'
    model = PurchasesModel
    success_url = 'finance:manage_purchases'
    values_list = 'invoice_no'
