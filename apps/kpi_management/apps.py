from django.apps import AppConfig


class KpiManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.kpi_management'

    def ready(self):
        """Import signals when app is ready"""
        try:
            import apps.kpi_management.signals  # noqa
        except ImportError:
            pass

