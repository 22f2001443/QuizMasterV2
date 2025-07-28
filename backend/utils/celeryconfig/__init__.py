from celery.schedules import crontab
import os

# Redis as broker and result backend
broker_url = os.getenv("REDIS_URL","redis://localhost:6379/0")
result_backend = os.getenv("REDIS_URL","redis://localhost:6379/0")

# Optional: Keep track of task starts
task_track_started = True

# Optional: Enable retry mechanisms and rate limiting if needed
task_acks_late = True
worker_prefetch_multiplier = 1

# Timezone and UTC setting
timezone = 'Asia/Kolkata'
enable_utc = True

# Periodic Task Schedules (Used by Celery Beat)
beat_schedule = {
    'send-daily-quiz-reminder': {
        'task': 'tasks.email_tasks.send_daily_quiz_reminders',
        'schedule': crontab(hour=9, minute=0),  # Every day at 9:00 AM
    },
    'send-monthly-performance-report': {
        'task': 'tasks.report_tasks.send_monthly_report_to_users',
        'schedule': crontab(day_of_month='1', hour=10, minute=0),  # 1st of every month at 10:00 AM
    }
}