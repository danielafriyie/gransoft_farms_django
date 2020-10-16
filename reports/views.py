from django.shortcuts import render
from django.views.generic import View

from mixins import PermissionRequiredMixin, ReportViewMixin
from finance.models import PurchasesModel, PurchasesModelAudit


def reports_home(request):
    return render(request, 'reports/reports.html')


class BasePurchasesReport(ReportViewMixin):
    exclude_kwargs = {'is_default': False}
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


class PurchasesReport(PermissionRequiredMixin, BasePurchasesReport, View):
    perm = 'finance.finance_pur_report'
    template = 'reports/purchase_report.html'
    excel_cols = (
        'purchase id' 'supplier name', 'phone', 'address', 'invoice number', 'date created',
        'quantity', 'unit price', 'amount', 'description',
    )
    query_cols = (
        'id', 'supplier_name', 'phone', 'address', 'invoice_no', 'date_created',
        'quantity', 'unit_price', 'amount', 'description',
    )
    model = PurchasesModel
    export_filename = 'purchases'


class PurchasesAuditReport(PermissionRequiredMixin, BasePurchasesReport, View):
    perm = 'finance.finance_pur_audit_trail'
    template = 'reports/purchase_autit_report.html'
    excel_cols = (
        'purchase id', 'supplier name', 'phone', 'address', 'invoice number', 'date created',
        'quantity', 'unit price', 'amount', 'action flag', 'auth user', 'description',
    )
    query_cols = (
        'purchase_id', 'supplier_name', 'phone', 'address', 'invoice_no', 'date_created',
        'quantity', 'unit_price', 'amount', 'action_flag', 'auth_user', 'description',
    )
    model = PurchasesModelAudit
    export_filename = 'purchases audit'
