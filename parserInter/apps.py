from django.apps import AppConfig


class ParserinterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'parserInter'

    def ready(self):
        import parserInter.signals
