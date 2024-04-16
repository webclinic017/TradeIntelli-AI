from celery import Celery
from celery.schedules import crontab

from alerts import Alerts

app = Celery(
    'worker',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0',
    include=['celery_app']
)


@app.task
def test_task():
    Alerts.run_alerts()
    pass

# After defining your 'app' (Celery instance) and tasks

app.conf.beat_schedule = {
    'test-task-every-5-minutes': {
        'task': 'celery_app.test_task',
        'schedule': crontab(minute='*/5'),
    },
}