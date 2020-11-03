from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib import messages as msg

from datetime import datetime as dt

from mixins import PermissionRequiredMixin, DeleteModelObjectMixin, ModuleAccesRedirectMixin, ManageModuleViewMixin
from .forms import (
    CreateFinanceForm, UpdateFinanceForm, CreateFinanceItemDetailFormSet, UpdateFinanceItemDetailFormSet
)
from .models import FinanceModel, ItemDetail


class MainModuleMixin(ModuleAccesRedirectMixin, View):
    perm_link = (
        ('finance:create', 'finance.finance_add_new'),
        ('finance:manage', 'finance.finance_update'),
    )


class CreateFinanceItemView(PermissionRequiredMixin, View):
    perm = 'finance.finance_add_new'

    def get(self, request):
        return render(request, 'finance/sales_purchases/create.html', {
            'form': CreateFinanceForm(initial={'auth_user': self.request.user}),
            'item_detail_form_set': CreateFinanceItemDetailFormSet(queryset=ItemDetail.objects.none()),
        })

    def post(self, request):
        form = CreateFinanceForm(request.POST)
        item_detail_form_set = CreateFinanceItemDetailFormSet(data=request.POST)
        if form.is_valid() and item_detail_form_set.is_valid():
            item_detail_form_set.instance = form.save()
            item_detail_form_set.save()
            msg.success(request, 'Created successfully!')
            return redirect('finance:create')
        msg.error(request, 'There\'s an error in your form!')
        return render(request, 'finance/sales_purchases/create.html', {
            'form': form,
            'item_detail_form_set': item_detail_form_set
        })


class UpdateFinanceItemView(PermissionRequiredMixin, View):
    perm = 'finance.finance_update'
    template = 'finance/sales_purchases/update.html'

    def get(self, request):
        finance_item = get_object_or_404(FinanceModel, invoice_no=request.GET['inv_no'])
        form = UpdateFinanceForm(instance=finance_item)
        item_detail_form_set = UpdateFinanceItemDetailFormSet(instance=finance_item)
        return render(request, self.template, {
            'form': form,
            'item_detail_form_set': item_detail_form_set,
        })

    def post(self, request):
        finance_item = get_object_or_404(FinanceModel, invoice_no=request.POST['inv_no'], pk=request.POST['p_id'])
        form, prev_path = UpdateFinanceForm(request.POST), request.POST['prev-path']
        item_detail_form_set = UpdateFinanceItemDetailFormSet(data=request.POST, instance=finance_item)
        if form.is_valid() and item_detail_form_set.is_valid():
            form.save(request.user, request.POST['p_id'], request.POST['inv_no'])
            item_detail_form_set.save()
            msg.success(request, 'Updated successfully!')
            return redirect(prev_path) if prev_path else redirect('finance:manage_purchases')
        msg.error(request, 'There\'s an error in your form!')
        return render(request, self.template, {
            'form': form,
            'item_detail_form_set': item_detail_form_set,
        })


class ManageFinanceItemView(PermissionRequiredMixin, ManageModuleViewMixin, View):
    perm = 'finance.finance_update'
    template = 'finance/sales_purchases/manage.html'
    model = FinanceModel
    values_list_cols = ('id', 'supplier_name', 'phone', 'address', 'invoice_no', 'category', 'date_created')
    order_col = '-date_created'
    url_filter_kwargs = (('category', 'category'),)

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


class DeleteFinanceItemView(PermissionRequiredMixin, DeleteModelObjectMixin, View):
    perm = 'finance.finance_delete'
    model = FinanceModel
    values_list = 'invoice_no'

    @property
    def get_success_url(self):
        return self.request.POST['path']
