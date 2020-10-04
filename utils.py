from django.contrib.auth.models import Permission
from django.shortcuts import get_object_or_404
from django.conf import settings

from exceptions_ import ImmutableUserError, UnmatchedPkError

User = settings.AUTH_USER_MODEL


def toggle_admin(user: User, obj: bool) -> None:
    """
        Assign or remove admin privileges of the user.
        obj parameter is data from the frontend, mostly boolean
    """
    user.is_admin = True if obj else False
    user.save()


def toggle_role(user: User, obj: bool, perm: str) -> None:
    """
        Assign and update role to a given user.
        obj parameter is data from frontend, mostly boolean
    """
    try:
        p = get_object_or_404(Permission, codename=perm.split('.')[1])
        if obj:
            None if user.has_perm(perm) else user.user_permissions.add(p)
        else:
            user.user_permissions.remove(p) if user.has_perm(perm) else None
    except IndexError:
        raise


def assign_user_roles(user: User, roles: dict) -> None:
    toggle_admin(user, roles.get('admin', False))

    toggle_role(user, roles.get('user_create', False), 'user_accounts.add_user')
    toggle_role(user, roles.get('user_update', False), 'user_accounts.update_user')
    toggle_role(user, roles.get('user_delete', False), 'user_accounts.delete_user')


def toggle_user_status(user: User, auth_user: User) -> None:
    """
    change user status to active or in-active
    :param user: user whose status is being toggled
    :param auth_user: user making the request
    :return:
    """
    user.is_active = False if user.is_active else True
    user.auth_user = auth_user
    user.save()


def get_user_perms(user: User) -> dict:
    return {
        'admin': user.is_admin,
        'user_create': user.has_perm('user_accounts.add_user'),
        'user_update': user.has_perm('user_accounts.update_user'),
        'user_delete': user.has_perm('user_accounts.delete_user'),
    }


def check_is_immutable(user: User) -> bool:
    """check if user account is immutable: cannot be changed or modified"""
    return user.is_immutable is True


def assert_immutable_user(user: User) -> None:
    if check_is_immutable(user):
        raise ImmutableUserError('Cannot modify or delete immutable user!')


def assert_unmatched_pk(pk1: int or str, pk2: int or str) -> None:
    try:
        assert int(pk1) == int(pk2)
    except AssertionError:
        raise UnmatchedPkError(f'{pk1} != {pk2}')
