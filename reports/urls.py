from django.urls import path, include
from .views import (
    PurchasesReport, reports_home, PurchasesAuditReport
)

app_name = 'reports'

home_url = [path('', reports_home, name='reports_home')]

finance_report_urls = [
    path('purchases-reports/', include([
        path('purchases/', PurchasesReport.as_view(), name='purchase_report'),
        path('purchases-audit/', PurchasesAuditReport.as_view(), name='purchase_audit_report')
    ]))
]

urlpatterns = home_url + finance_report_urls
