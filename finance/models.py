from django.db import models
from django.conf import settings
from django.urls import reverse

User = settings.AUTH_USER_MODEL


class BasePurchasesModel(models.Model):
    supplier_name = models.CharField(max_length=60)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=35)
    quantity = models.FloatField()
    unit_price = models.FloatField()
    amount = models.FloatField()
    description = models.TextField()
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.invoice_no

    def get_absolute_url(self):
        return reverse('finance:update_purchase', args=[str(self.id)])


class PurchasesModel(BasePurchasesModel):
    invoice_no = models.CharField(max_length=35, unique=True)
    auth_user = models.ForeignKey(User, on_delete=models.RESTRICT)

    class Meta:
        permissions = (
            ('finance_pur_add_new', 'Can create purchase custom'),
            ('finance_pur_update', 'Can update purchase custom'),
            ('finance_pur_delete', 'Can delete purchase custom'),
            ('finance_pur_audit_trail', 'Can view purchase audit trail custom')
        )
        ordering = ['id']
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'
        db_table = 'purchases_model'


class PurchasesModelAudit(BasePurchasesModel):
    invoice_no = models.CharField(max_length=35)
    purchase_id = models.IntegerField()
    auth_user = models.IntegerField()
    action_flag = models.CharField(max_length=20)

    class Meta:
        ordering = ['id']
        verbose_name = 'Purchase Audit'
        verbose_name_plural = 'Purchases Audit'
        db_table = 'purchases_audit_model'