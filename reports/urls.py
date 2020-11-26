from django.urls import path, include
from .views import (
    FinanceReportView, reports_home, FinanceAuditReportView, PenhouseReportView,
    BirdsStockReportView, MortalityCullReportView, MedicineFeedReportView, EggsReportView,
    EggsAuditReportView
)

app_name = 'reports'

home_url = [path('', reports_home, name='reports_home')]

finance_report_urls = [
    path('finance/', include([
        path('sales-purchases/', FinanceReportView.as_view(), name='sales_purchases'),
        path('finance-audit/', FinanceAuditReportView.as_view(), name='finance_audit_report')
    ]))
]

birds_report_urls = [
    path('birds/', include([
        path('penhouse/', PenhouseReportView.as_view(), name='penhouse_report'),
        path('stock/', BirdsStockReportView.as_view(), name='birds_stock_report'),
        path('mort-cull/', MortalityCullReportView.as_view(), name='mort_cull_report'),
        path('med-feed/', MedicineFeedReportView.as_view(), name='med_feed_report')
    ]))
]

eggs_report_urls = [
    path('eggs/', include([
        path('eggs/', EggsReportView.as_view(), name='eggs_report'),
        path('eggs-audit/', EggsAuditReportView.as_view(), name='eggs_audit_report'),
    ]))
]

urlpatterns = home_url + finance_report_urls + birds_report_urls + eggs_report_urls
