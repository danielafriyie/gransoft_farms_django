from django.contrib.auth.models import Permission
from exceptions_ import ImmutableUserError, UnmatchedPkError


def _group_has_perm(group, perm):
    try:
        group.permissions.get(codename=perm)
        return True
    except Permission.DoesNotExist:
        return False


def get_group_perms(group):
    return {
        'name': group.name,
        'add_user': _group_has_perm(group, 'add_user'),
        'update_user': _group_has_perm(group, 'update_user'),
        'delete_user': _group_has_perm(group, 'delete_user'),
        'set_password': _group_has_perm(group, 'set_password'),
        'manage_roles': _group_has_perm(group, 'manage_roles'),
        'view_user_account_audit_trail': _group_has_perm(group, 'view_user_account_audit_trail'),
        'finance_pur_add_new': _group_has_perm(group, 'finance_pur_add_new'),
        'finance_pur_update': _group_has_perm(group, 'finance_pur_update'),
        'finance_pur_delete': _group_has_perm(group, 'finance_pur_delete'),
        'finance_pur_audit_trail': _group_has_perm(group, 'finance_pur_audit_trail')
    }


def toggle_user_status(user, auth_user):
    """
    change user status to active or in-active
    :param user: user whose status is being toggled
    :param auth_user making the request
    :return:
    """
    user.is_active = False if user.is_active else True
    user.auth_user = auth_user
    user.save()


def check_is_immutable(user):
    """check if user account is immutable: cannot be changed or modified"""
    return user.is_immutable is True


def assert_immutable_user(user):
    if check_is_immutable(user):
        raise ImmutableUserError('Cannot modify or delete immutable user!')


def assert_unmatched_pk(pk1, pk2):
    try:
        assert int(pk1) == int(pk2)
    except AssertionError:
        raise UnmatchedPkError(f'{pk1} != {pk2}')
