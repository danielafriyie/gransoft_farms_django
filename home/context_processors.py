from django.contrib import admin
from .models import CompanyConfig


def company_config_processor(request):
    return {'company': CompanyConfig.objects.order_by('-id').all().first()}

