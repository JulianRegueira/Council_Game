from celery import shared_task
from .models import Heroe

@shared_task
def regenerar_energia():
    heroes = Heroe.objects.all()
    for heroe in heroes:
        heroe.regenerar_energia()
