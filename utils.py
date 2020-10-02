from django.contrib.auth.models import Permission
from django.shortcuts import get_object_or_404


def toggle_admin(user, obj: bool) -> None:
    """
        Assign or remove admin privileges of the user.
        obj parameter is data from the frontend, mostly boolean
    """
    user.is_admin = True if obj else False
    user.save()


def toggle_role(user, obj: bool, perm: str) -> None:
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


def assign_user_roles(user, roles: dict) -> None:
    toggle_admin(user, roles.get('admin', False))

    toggle_role(user, roles.get('user_create', False), 'user_accounts.add_user')
    toggle_role(user, roles.get('user_update', False), 'user_accounts.update_user')
    toggle_role(user, roles.get('user_delete', False), 'user_accounts.delete_user')
