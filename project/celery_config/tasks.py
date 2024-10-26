# celery
from celery import shared_task
from celery_config.controllers import mejores_3, obtener_requests

import time

@shared_task
def wait_and_return():
    time.sleep(20)
    return 'Hello World!'

@shared_task
def recommendation(id_usuario):
    return id_usuario