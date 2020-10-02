from django.db.models.signals import pre_save, pre_delete
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils.timezone import now
from django.shortcuts import get_object_or_404

from .models import UserAccountsModel, UserAccountsModelAudit, UsersAuthenticationLog
from logger import auth_log


def co_user_accounts_audit(instance, action):
    # if instance.pk == 1:
    #     raise ValueError('cannot modify super admin')
    UserAccountsModelAudit.objects.create(
        username=instance.username,
        auth_user=instance.auth_user.pk,
        name=instance.name,
        phone_no=instance.phone_no,
        gender=instance.gender,
        date_of_birth=instance.date_of_birth,
        date_created=instance.date_created,
        is_admin=instance.is_admin,
        is_active=instance.is_active,
        is_staff=instance.is_staff,
        is_superuser=instance.is_superuser,
        action_flag=action
    )


@receiver(pre_save, sender=UserAccountsModel)
def user_accounts_pre_save(sender, instance, **kwargs):
    if instance._state.adding:
        co_user_accounts_audit(instance=instance, action='Insert')
    else:
        qs = get_object_or_404(UserAccountsModel, username=instance.username)
        try:
            assert qs.username == instance.username
            assert qs.name == instance.name
            assert qs.phone_no == instance.phone_no
            assert qs.gender == instance.gender
            assert qs.date_of_birth == instance.date_of_birth
            assert qs.date_created == instance.date_created
            assert qs.is_admin == instance.is_admin
            assert qs.is_active == instance.is_active
            assert qs.is_staff == instance.is_staff
            assert qs.is_superuser == instance.is_superuser
            assert qs.auth_user == instance.auth_user
        except AssertionError:
            co_user_accounts_audit(instance=instance, action='Update')


@receiver(pre_delete, sender=UserAccountsModel)
def user_accounts_pre_delete(sender, instance, **kwargs):
    co_user_accounts_audit(instance=instance, action='Delete')


@receiver(user_logged_in)
def sig_user_logged_in(sender, user, request, **kwargs):
    auth_log().info(f"{user.username} logged in at {request.META['REMOTE_ADDR']}")
    UsersAuthenticationLog.objects.create(auth_user=user, last_login=now())


@receiver(user_logged_out)
def sig_user_logged_out(sender, user, request, **kwargs):
    auth_log().info(f"{user.username} logged out at {request.META['REMOTE_ADDR']}")
    last_row = UsersAuthenticationLog.objects.filter(auth_user=user).last()
    UsersAuthenticationLog.objects.filter(auth_user=user, pk=last_row.pk).update(last_logout=now())
