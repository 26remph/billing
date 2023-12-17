from celery import shared_task


@shared_task
def clearing(
    name="read_from_external_api",
    bind=True,
    acks_late=True,
    autoretry_for=(Exception,),
    max_retries=5,
    retry_backoff=True,
    retry_backoff_max=500,
    retry_jitter=True,
):
    # read from billing db
    ...
