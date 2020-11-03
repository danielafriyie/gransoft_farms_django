from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from .models import FinanceModelAudit, ItemDetail


def _create_finance_audit(instance, action):
    FinanceModelAudit.objects.create(
        supplier_name=instance.invoice_no.supplier_name,
        phone=instance.invoice_no.phone,
        address=instance.invoice_no.address,
        date_created=instance.invoice_no.date_created,
        invoice_no=instance.invoice_no.invoice_no,
        item_id=instance.invoice_no.pk,
        auth_user=instance.invoice_no.auth_user.username,
        is_default=instance.invoice_no.is_default,
        action_flag=action,
        quantity=instance.quantity,
        unit_price=instance.unit_price,
        amount=instance.amount,
        description=instance.description,
        category=instance.invoice_no.category
    )


@receiver(pre_save, sender=ItemDetail)
def sig_finance_pre_save(sender, instance, **kwargs):
    if instance._state.adding:
        _create_finance_audit(instance, 'insert')
    else:
        _create_finance_audit(instance, 'update')


@receiver(pre_delete, sender=ItemDetail)
def sig_finance_pre_delete(sender, instance, **kwargs):
    _create_finance_audit(instance, 'Delete')
