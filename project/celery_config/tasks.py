# celery
from celery import shared_task
from celery_config.controllers import mejores_3, obtener_requests, obtener_proximos_partidos, aciertos_por_team

import time

@shared_task
def recommendation(id):
    return aciertos_por_team(obtener_requests(id))

