# celery
from celery import shared_task
from celery_config.controllers import mejores_3, obtener_requests, obtener_proximos_partidos, aciertos_por_team, ponderador_por_fixtures

import time

@shared_task
def recommendation(id):
    return mejores_3(id)

