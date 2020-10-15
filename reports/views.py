from django.shortcuts import render
from django.views.generic import View

from mixins import PermissionRequiredMixin, ReportViewMixin
from finance.models import PurchasesModel, PurchasesModelAudit


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
        'supplier_name', 'phone', 'address', 'invoice_no', 'date_created',
        'quantity', 'unit_price', 'amount', 'description',
    )
    model = PurchasesModel
    exclude_kwargs = {'is_default': False}
    order_col = '-date_created'
    export_filename = 'purchases'


class PurchasesAuditReport(PermissionRequiredMixin, ReportViewMixin, View):
    perm = 'finance.finance_pur_audit_trail'
    template = 'reports/purchase_autit_report.html'
    excel_cols = (
        'supplier name', 'phone', 'address', 'invoice number', 'date created',
        'quantity', 'unit price', 'amount', 'action flag', 'auth user', 'description',
    )
    query_cols = (
        'supplier_name', 'phone', 'address', 'invoice_no', 'date_created',
        'quantity', 'unit_price', 'amount', 'action_flag', 'auth_user', 'description',
    )
    model = PurchasesModelAudit
    exclude_kwargs = {'is_default': False}
    order_col = '-date_created'
    export_filename = 'purchases audit'
