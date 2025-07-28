# If you need to run beat as a separate CLI command
from utils.celeryconfig.celery_worker import celery

if __name__ == "__main__":
    celery.start(argv=["celery", "beat", "--loglevel=info"])