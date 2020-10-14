from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib import messages as msg
from django.core.paginator import Paginator

from datetime import datetime as dt

from mixins import PermissionRequiredMixin, DeleteModelObjectMixin
from .forms import CreatePurchaseForm, UpdatePurchaseForm
from .models import PurchasesModel


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


class ManagePurchases(PermissionRequiredMixin, View):
    perms = ['finance.finance_pur_update', 'finance.finance_pur_add_new', 'finance.finance_pur_delete']

    def get(self, request):
        return render(request, 'finance/purchases/manage_purchases.html', self.context)

    @staticmethod
    def purchase_data(**filtering):
        cols = (
            'id', 'supplier_name', 'phone', 'address', 'invoice_no', 'date_created',
            'quantity', 'unit_price', 'amount'
        )
        return PurchasesModel.objects.order_by('-date_created').values_list(*cols).filter(**filtering, is_default=False)

    @property
    def query_set(self):
        cd = dt.now().date()  # current date
        qs = self.purchase_data(date_created__gte=cd, date_created__lte=cd)

        if ('date1' and 'date2') in self.request.GET:
            d1, d2 = self.request.GET['date1'], self.request.GET['date2']
            qs = self.purchase_data(date_created__gte=d1, date_created__lte=d2)

        if 'search' in self.request.GET:
            search = self.request.GET['search']
            qs = self.purchase_data(invoice_no__icontains=search)
            if not qs:
                qs = self.purchase_data(supplier_name__icontains=search)
        return qs

    @property
    def context(self):
        paginator, page = Paginator(self.query_set, 25), self.request.GET.get('page')
        paginator_pages = paginator.get_page(page)
        return {
            'paginator_pages': paginator_pages,
            'values': self.request.GET
        }


class DeletePurchase(PermissionRequiredMixin, DeleteModelObjectMixin, View):
    perm = 'finance.finance_pur_delete'
    model = PurchasesModel
    success_url = 'finance:manage_purchases'
    values_list = 'invoice_no'
