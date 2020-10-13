from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class BasePurchasesModel(models.Model):
    supplier_name = models.CharField(max_length=60),
    phone = models.CharField(max_length=15),
    address = models.CharField(max_length=35),
    invoice_no = models.CharField(max_length=35),
    quantity = models.FloatField(),
    unit_price = models.FloatField(),
    amount = models.FloatField(),
    des_cription = models.TextField(),
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class PurchasesModel(BasePurchasesModel):
    invoice_no = models.CharField(max_length=35, unique=True)
    auth_user = models.ForeignKey(User, on_delete=models.RESTRICT),

    class Meta:
        ordering = ['id']
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'
        db_table = 'purchases_model'


class PurchasesModelAudit(BasePurchasesModel):
    purchase_id = models.IntegerField()
    auth_user = models.IntegerField(),
    action_flag = models.CharField(max_length=20)

    class Meta:
        ordering = ['id']
        verbose_name = 'Purchase Audit'
        verbose_name_plural = 'Purchases Audit'
        db_table = 'purchases_audit_model'
