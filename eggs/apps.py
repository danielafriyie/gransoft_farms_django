from django.apps import AppConfig


class EggsConfig(AppConfig):
    name = 'eggs'

    def ready(self):
        import eggs.signals
