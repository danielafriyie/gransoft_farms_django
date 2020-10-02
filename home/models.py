from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class CompanyConfig(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    contact = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    auth_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-id']
        db_table = 'company_config_model'
        verbose_name = 'Company Configuration'
        verbose_name_plural = 'Company Configurations'

    def __str__(self):
        return self.name
