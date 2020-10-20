from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from .models import PurchaseModelAudit, PurchaseDetail


def _create_purchase_audit(instance, action):
    PurchaseModelAudit.objects.create(
        supplier_name=instance.invoice_no.supplier_name,
        phone=instance.invoice_no.phone,
        address=instance.invoice_no.address,
        date_created=instance.invoice_no.date_created,
        invoice_no=instance.invoice_no,
        purchase_id=instance.invoice_no.pk,
        auth_user=instance.invoice_no.auth_user.username,
        is_default=instance.invoice_no.is_default,
        action_flag=action,
        quantity=instance.quantity,
        unit_price=instance.unit_price,
        amount=instance.amount,
        description=instance.description
    )


@receiver(pre_save, sender=PurchaseDetail)
def sig_purchases_post_save(sender, instance, **kwargs):
    if instance._state.adding:
        _create_purchase_audit(instance, 'insert')
    else:
        _create_purchase_audit(instance, 'update')


@receiver(pre_delete, sender=PurchaseDetail)
def sig_purchase_pre_delete(sender, instance, **kwargs):
    _create_purchase_audit(instance, 'Delete')
