from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import PurchasesModel, PurchasesModelAudit


def _create_purcase_audit(instance, action):
    PurchasesModelAudit.objects.create(
        supplier_name=instance.supplier_name,
        phone=instance.phone,
        address=instance.address,
        quantity=instance.quantity,
        unit_price=instance.unit_price,
        amount=instance.amount,
        description=instance.description,
        date_created=instance.date_created,
        invoice_no=instance.invoice_no,
        purchase_id=instance.pk,
        auth_user=instance.auth_user.pk,
        action_flag=action
    )


@receiver(post_save, sender=PurchasesModel)
def sig_purchases_pre_save(sender, instance, **kwargs):
    _create_purcase_audit(instance, 'insert or update')


@receiver(pre_delete, sender=PurchasesModel)
def sig_purchase_pre_delete(sender, instance, **kwargs):
    _create_purcase_audit(instance, 'Delete')
