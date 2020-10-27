from django.shortcuts import render
from django.views.generic import View

from mixins import PermissionRequiredMixin, ReportViewMixin
from finance.models import PurchaseModelAudit, PurchaseDetail


def reports_home(request):
    return render(request, 'reports/reports.html')


class PurchasesReport(PermissionRequiredMixin, ReportViewMixin, View):
    perm = 'finance.finance_pur_report'
    template = 'reports/purchase_report.html'
    excel_cols = (
        'supplier name', 'phone', 'address', 'invoice number', 'date created',
        'quantity', 'unit price', 'amount', 'description',
    )
    query_cols = (
        'invoice_no__supplier_name', 'invoice_no__phone', 'invoice_no__address', 'invoice_no',
        'invoice_no__date_created', 'quantity', 'unit_price', 'amount', 'description'
    )
    exclude_kwargs = {'invoice_no__is_default': False}
    model = PurchaseDetail
    export_filename = 'purchases'
    order_col = '-invoice_no__date_created'
    filter_date_field = 'invoice_no__date_created'

    @property
    def query_set(self):
        qs = super().query_set
        if 'search' in self.request.GET and self.request.GET['search']:
            search = self.request.GET['search']
            qs = super().query_set.filter(invoice_no__invoice_no__icontains=search)
            if not qs:
                qs = super().query_set.filter(invoice_no__supplier_name__icontains=search)
        return qs


class PurchasesAuditReport(PermissionRequiredMixin, ReportViewMixin, View):
    perm = 'finance.finance_pur_audit_trail'
    template = 'reports/purchase_autit_report.html'
    exclude_kwargs = {'is_default': False}
    excel_cols = (
        'supplier name', 'phone', 'address', 'invoice number', 'date created',
        'quantity', 'unit price', 'amount', 'action flag', 'auth user', 'description',
    )
    query_cols = (
        'supplier_name', 'phone', 'address', 'invoice_no', 'date_created',
        'quantity', 'unit_price', 'amount', 'action_flag', 'auth_user', 'description',
    )
    model = PurchaseModelAudit
    export_filename = 'purchases audit'
    order_col = '-date_created'

    @property
    def query_set(self):
        qs = super().query_set
        if 'search' in self.request.GET and self.request.GET['search']:
            search = self.request.GET['search']
            qs = qs.filter(invoice_no__icontains=search)
            if not qs:
                qs = super().query_set.filter(supplier_name__icontains=search)
        return qs
