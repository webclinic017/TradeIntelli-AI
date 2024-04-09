from celery import Celery
from celery.schedules import crontab

app = Celery(
    'worker',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0',
    include=['app.celery_app']
)


@app.task
def test_task():
    print("Test task executed")


# After defining your 'app' (Celery instance) and tasks

app.conf.beat_schedule = {
    'test-task-every-5-minutes': {
        'task': 'app.celery_app.test_task',
        'schedule': crontab(minute='*/5'),
    },
}