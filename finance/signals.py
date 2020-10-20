from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import PurchaseModel, PurchaseModelAudit, PurchaseDetail, PurchaseDetailAudit


def _create_purchase_audit(instance, action):
    PurchaseModelAudit.objects.create(
        supplier_name=instance.supplier_name,
        phone=instance.phone,
        address=instance.address,
        date_created=instance.date_created,
        invoice_no=instance.invoice_no,
        purchase_id=instance.pk,
        auth_user=instance.auth_user.username,
        is_default=instance.is_default,
        action_flag=action
    )


def _create_purchase_detail_audit(instance):
    PurchaseDetailAudit.objects.create(
        invoice_no=instance.invoice_no,
        quantity=instance.quantity,
        unit_price=instance.unit_price,
        amount=instance.amount,
        description=instance.description
    )


@receiver(post_save, sender=PurchaseModel)
def sig_purchases_post_save(sender, instance, **kwargs):
    _create_purchase_audit(instance, 'insert or update')


@receiver(pre_delete, sender=PurchaseModel)
def sig_purchase_pre_delete(sender, instance, **kwargs):
    _create_purchase_audit(instance, 'Delete')


@receiver(post_save, sender=PurchaseDetail)
def sig_purchase_detail_post_save(sender, instance, **kwargs):
    _create_purchase_detail_audit(instance)


@receiver(pre_delete, sender=PurchaseDetail)
def sig_purchase_detail_pre_delete(sender, instance, **kwargs):
    _create_purchase_detail_audit(instance)
