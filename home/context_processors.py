from .models import CompanyConfig


def company_config_processor(request):
    return {'company': CompanyConfig.objects.order_by('-id').all().first()}


def _any(user, perms):
    return any([user.has_perm(perm) for perm in perms])


def menu_processor(request):
    user = request.user
    menu = {}
    purchases_perms = [
        'finance.finance_pur_add_new', 'finance.finance_pur_update',
        'finance.finance_pur_delete'
    ]
    menu['purchases_menu'] = _any(user, purchases_perms)

    sales_perms = [
        'finance.finance_sal_add_new', 'finance.finance_sal_update',
        'finance.finance_sal_delete'
    ]
    menu['sales_menu'] = _any(user, sales_perms)
    return menu
