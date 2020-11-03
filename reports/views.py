from django.shortcuts import render
from django.views.generic import View

from mixins import PermissionRequiredMixin, ReportViewMixin
from finance.models import FinanceModelAudit, ItemDetail


def reports_home(request):
    return render(request, 'reports/reports.html')


class FinanceReport(PermissionRequiredMixin, ReportViewMixin, View):
    perm = 'finance.finance_report'
    template = 'reports/purchase_sale_report.html'
    excel_cols = (
        'supplier name', 'phone', 'address', 'invoice number', 'category', 'date created',
        'quantity', 'unit price', 'amount', 'description',
    )
    query_cols = (
        'invoice_no__supplier_name', 'invoice_no__phone', 'invoice_no__address', 'invoice_no',
        'invoice_no__category', 'invoice_no__date_created', 'quantity', 'unit_price', 'amount', 'description'
    )
    exclude_kwargs = {'invoice_no__is_default': False}
    model = ItemDetail
    export_filename = 'finance_report'
    order_col = '-invoice_no__date_created'
    filter_date_field = 'invoice_no__date_created'
    url_filter_kwargs = (('category', 'invoice_no__category'),)

    @property
    def query_set(self):
        qs = super().query_set
        if 'search' in self.request.GET and self.request.GET['search']:
            search = self.request.GET['search']
            qs = qs.filter(invoice_no__invoice_no__icontains=search)
            if not qs:
                qs = super().query_set.filter(invoice_no__supplier_name__icontains=search)
        return qs


class FinanceAuditReport(PermissionRequiredMixin, ReportViewMixin, View):
    perm = 'finance.finance_audit_trail'
    template = 'reports/purchase_sale_autit_report.html'
    exclude_kwargs = {'is_default': False}
    excel_cols = (
        'supplier name', 'phone', 'address', 'invoice number', 'category', 'date created',
        'quantity', 'unit price', 'amount', 'action flag', 'auth user', 'description',
    )
    query_cols = (
        'supplier_name', 'phone', 'address', 'invoice_no', 'category', 'date_created',
        'quantity', 'unit_price', 'amount', 'action_flag', 'auth_user', 'description',
    )
    model = FinanceModelAudit
    export_filename = 'finance_audit_report'
    order_col = '-date_created'
    url_filter_kwargs = (('category', 'category'),)

    @property
    def query_set(self):
        qs = super().query_set
        if 'search' in self.request.GET and self.request.GET['search']:
            search = self.request.GET['search']
            qs = qs.filter(invoice_no__icontains=search)
            if not qs:
                qs = super().query_set.filter(supplier_name__icontains=search)
        return qs
