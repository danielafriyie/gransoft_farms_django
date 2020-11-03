from django.urls import path, include
from .views import (
    FinanceReport, reports_home, FinanceAuditReport
)

app_name = 'reports'

home_url = [path('', reports_home, name='reports_home')]

finance_report_urls = [
    path('finance/', include([
        path('sales-purchases/', FinanceReport.as_view(), name='sales_purchases'),
        path('finance-audit/', FinanceAuditReport.as_view(), name='finance_audit_report')
    ]))
]

urlpatterns = home_url + finance_report_urls
