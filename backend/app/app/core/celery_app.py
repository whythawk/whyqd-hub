from celery import Celery, signals

celery_app = Celery("worker", broker="amqp://guest@queue//")

celery_app.conf.task_routes = {"app.worker.*": "main-queue"}


@signals.setup_logging.connect
def setup_celery_logging(**kwargs):
    # https://docs.celeryq.dev/en/stable/userguide/signals.html?highlight=%40signals
    # https://github.com/ray-project/ray/issues/8610
    worker_redirect_stdouts = False  # noqa: F841
