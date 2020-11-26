from django.shortcuts import render
from django.db import connection
from django.views.generic import View

from mixins import PermissionRequiredMixin, ReportViewMixin
from finance.models import FinanceModelAudit, ItemDetail
from birds.models import BirdsStock, MortalityCull, MedicineFeed
from eggs.models import EggsModel, EggsModelAudit


def reports_home(request):
    return render(request, 'reports/reports.html')


class BaseReportView(PermissionRequiredMixin, ReportViewMixin, View):
    pass


class FinanceReportView(BaseReportView):
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


class FinanceAuditReportView(BaseReportView):
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


class PenhouseReportView(BaseReportView):
    perm = 'birds.birds_manage_pen_house'
    template = 'reports/penhouse_report.html'
    excel_cols = ('id', 'date created', 'pen number', 'pen name', 'number of birds', 'auth user',)
    export_filename = 'penhouse report'

    @property
    def query_set(self):
        if 'search' in self.request.GET and self.request.GET['search']:
            return self.query_set_data(self.request.GET['search'])
        return self.query_set_data()

    def query_set_data(self, pen_name=''):
        sql = """
        SELECT 
            p.id,
            p.date_created,
            p.pen_number,
            p.pen_name,
            SUM(b.quantity) AS total_birds,
            u.username
        FROM
            penhouse_model p
                LEFT JOIN
            birds_stock_model b ON p.pen_number = b.pen_house_id
                LEFT JOIN
            user_accounts_model u ON u.id = p.auth_user_id
        WHERE p.pen_name LIKE '%{}%'
        GROUP BY p.id;
        """.format(pen_name)
        with connection.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()


class BirdsStockReportView(BaseReportView):
    perm = 'birds.birds_manage_birds_stock'
    template = 'reports/birds_stock_report.html'
    excel_cols = (
        'id', 'date_created', 'pen_house', 'invoice_no__invoice_no',
        'quantity', 'auth_user__username'
    )
    query_cols = excel_cols
    model = BirdsStock
    export_filename = 'birds stock report'
    url_filter_kwargs = (('search', 'pen_house__pen_name__icontains'),)


class MortalityCullReportView(BaseReportView):
    perm = 'birds.birds_can_manage_mortality_cull'
    template = 'reports/mort_cull_report.html'
    excel_cols = (
        'id', 'date_created', 'pen_house', 'category', 'quantity',
        'description', 'auth_user__username',
    )
    query_cols = excel_cols
    model = MortalityCull
    export_filename = 'mortality/cull report'
    url_filter_kwargs = (
        ('search', 'pen_house__pen_name__icontains'),
        ('category', 'category__icontains'),
    )


class MedicineFeedReportView(BaseReportView):
    perm = 'birds.birds_can_manage_mortality_cull'
    template = 'reports/medicine_feeds_report.html'
    excel_cols = (
        'id', 'date_created', 'pen_house', 'category', 'quantity',
        'description', 'auth_user__username',
    )
    query_cols = excel_cols
    model = MedicineFeed
    export_filename = 'medicine/feeds report'
    url_filter_kwargs = (
        ('search', 'pen_house__pen_name__icontains'),
        ('category', 'category__icontains'),
    )


class EggsReportView(BaseReportView):
    perm = 'egg.manage_eggs'
    template = 'reports/eggs_report.html'
    excel_cols = ('id', 'pen__pen_name', 'date_created', 'time', 'quantity', 'auth_user')
    query_cols = excel_cols
    model = EggsModel
    export_filename = 'eggs report'
    url_filter_kwargs = (('search', 'pen__pen_number__icontains'),)


class EggsAuditReportView(BaseReportView):
    perm = 'egg.manage_eggs_audit'
    template = 'reports/eggs_audit_report.html'
    excel_cols = ('id', 'egg_id', 'pen', 'date_created', 'time', 'quantity', 'action_flag', 'auth_user')
    query_cols = excel_cols
    model = EggsModelAudit
    export_filename = 'eggs audit report'
    url_filter_kwargs = (('search', 'pen__icontains'),)
