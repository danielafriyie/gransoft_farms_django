from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from .models import EggsModel, EggsModelAudit


def _create_egg_audit(sender, instance, action_flag, **kwargs):
    EggsModelAudit.objects.create(
        pen=instance.pen.pen_number,
        time=instance.time,
        quantity=instance.quantity,
        action_flag=action_flag,
        egg_id=instance.pk,
        auth_user=instance.auth_user.username
    )


@receiver(pre_save, sender=EggsModel)
def sig_eggs_pre_save(sender, instance, **kwargs):
    if instance._state.adding:
        _create_egg_audit(sender, instance, 'Insert', **kwargs)
    else:
        _create_egg_audit(sender, instance, 'Update', **kwargs)


@receiver(pre_delete, sender=EggsModel)
def sig_eggs_pre_delete(sender, instance, **kwargs):
    _create_egg_audit(sender, instance, 'Delete', **kwargs)
