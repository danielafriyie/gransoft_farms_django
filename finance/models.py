from django.db import models
from django.conf import settings
from django.urls import reverse

User = settings.AUTH_USER_MODEL


class BaseModel(models.Model):
    category_choices = (('Sale', 'Sale'), ('Purchase', 'Purchase'))
    supplier_name = models.CharField(max_length=60)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=35)
    is_default = models.BooleanField(default=False)
    category = models.CharField(max_length=10, choices=category_choices)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-date_created']

    def __str__(self):
        return f'{self.supplier_name} - {self.invoice_no}'


class FinanceModel(BaseModel):
    invoice_no = models.CharField(max_length=35, unique=True)
    auth_user = models.ForeignKey(User, on_delete=models.RESTRICT)

    class Meta:
        permissions = (
            ('finance_add_new', 'Can create custom'),
            ('finance_update', 'Can update custom'),
            ('finance_delete', 'Can delete custom'),
            ('finance_report', 'Can view report custom'),
            ('finance_audit_trail', 'Can view audit trail custom')
        )
        verbose_name = 'Sale / Purchase'
        verbose_name_plural = 'Sales / Purchases'
        db_table = 'finance_model'

    def get_absolute_url(self):
        return reverse('finance:update', args=[str(self.id)])


class ItemDetail(models.Model):
    invoice_no = models.ForeignKey(FinanceModel, on_delete=models.CASCADE, to_field='invoice_no')
    quantity = models.FloatField()
    unit_price = models.FloatField()
    amount = models.FloatField()
    description = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Item Detail'
        verbose_name_plural = 'Item Details'
        db_table = 'item_detail_model'


class FinanceModelAudit(BaseModel):
    invoice_no = models.CharField(max_length=35)
    item_id = models.IntegerField()
    quantity = models.FloatField(null=True, blank=True)
    unit_price = models.FloatField(null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    auth_user = models.CharField(max_length=35)
    action_flag = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Sale / Purchase Audit'
        verbose_name_plural = 'Sales / Purchases Audit'
        db_table = 'finance_model_audit'



