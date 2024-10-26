# FastAPI
from fastapi import FastAPI
from models import Id

# celery
from celery_config.tasks import recommendation

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World, this is a route from the producer or job master"}

# https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html

@app.get("/job/{id}")
def get_job(job_id: str):
    job = recommendation.AsyncResult(job_id)
    print(job)
    return {
        "ready": job.ready(),
        "result": job.result,
    }

@app.post("/job")
def post_publish_job(id: Id):
    job = recommendation.delay(id.id)
    return {
        "message": "job published",
        "job_id": job.id,
    }

@app.get("/heartbeat")
def heartbeat():
    return True
