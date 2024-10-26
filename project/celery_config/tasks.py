# celery
from celery import shared_task
from celery_config.controllers import mejores_3, obtener_requests

import time

@shared_task
def recommendation(id):
    return id