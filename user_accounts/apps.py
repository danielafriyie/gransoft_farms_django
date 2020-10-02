from django.apps import AppConfig


class UserAccountsConfig(AppConfig):
    name = 'user_accounts'

    def ready(self):
        import user_accounts.signals
