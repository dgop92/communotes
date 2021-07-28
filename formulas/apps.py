from django.apps import AppConfig


class FormulasConfig(AppConfig):
    name = "formulas"

    def ready(self) -> None:
        from formulas import signals

        return super().ready()
