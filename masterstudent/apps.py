from django.apps import AppConfig


class MasterstudentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'masterstudent'

    def ready(self):
        # Only run in dev server, not in migration/command mode
        import sys
        if 'runserver' in sys.argv:
            from .utils import load_students_from_excel
            load_students_from_excel()