from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Configura las variables de entorno Django para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Council_Game.settings')

app = Celery('Council_Game')

# Cargar la configuración de Django en Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-descubrir tareas en tus aplicaciones Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

app.conf.beat_schedule = {
    'regenerar-energia-cada-hora': {
        'task': 'tu_aplicacion.tasks.regenerar_energia',
        'schedule': crontab(minute=0, hour='*'),  # Cada hora
    },
}

