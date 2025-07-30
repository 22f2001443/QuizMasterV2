# It's all about the 'backend' -- Setup Guide

Here I have explained how to set up and run the backend of the application using multiple terminals.

---
0. Create `.env` file using `.env.example`

## Terminal 1 : Start the Backend Server

```bash
cd backend

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python3 app.py
#or
flask run --host=0.0.0.0 --port=8000
```

## Terminal 2 – Start Redis Server

```bash
cd backend/utils
redis-server redis-config.conf
```

## Terminal 3 –  Redis CLI (Optional)

```bash
redis-cli ping
redis-cli

# Inside Redis CLI
keys *

```
## Terminal 4 – Start python SMTP Server

```bash
cd backend
source venv/bin/activate

# Run a local debug SMTP server on port 1025
python3 -m aiosmtpd -n -l localhost:1025
```

## Terminal 5 – Start Celery Worker

```bash
cd backend
source venv/bin/activate

celery -A utils.celeryconfig.celery_worker.celery worker --loglevel=info
```

## Terminal 6 – Start Celery Beat Scheduler

```bash
cd backend
source venv/bin/activate

celery -A utils.celeryconfig.celery_worker.celery beat --loglevel=info
```
or
```bash
cd backend
source venv/bin/activate

python3 utils/celeryconfig/celery_beat.py
```

### File Structure:

```
Backend/
├── requirements.txt                            # List of python package on needed for the app to run (dependencies)
├── .env                                        # Environment variables
├── .env.example                                # Template for environment variables
├── .gitignore                                  # Files/folders to be ignored by Git
├── README.md                                   # Project documentation (this file)
├── app.py                                      # Entry point of the Flask app (Main app); .env, Sem seed, app, cache clr, db, CORS
├── data/
│   ├── quiz-db-v2.sqlite                       # SQLite Database
│   ├── dump.rdb                                # Redis Dumb db, relocated here by redis-config.conf
│   ├── celerybeat-schedule.db                  # Celery beat schedule state; This is not actually coming here & storing in root Backend
│   └── backup/                                 # This is the backup of the data stored in DB; incase I have to delete the .sqlite file
│       ├── backup-creation.sql
│       └── backup-data.sql
├── utils/                                      # All the configuration files are being stored here
│   ├── redis-config.conf                       # Redis server configuration
│   ├── config.py                               # General app configuration; desides db file's location
│   └── CeleryConfig/
│       ├── __init__.py                         # Celery-specific configuration
│       ├── celery-beat.py                      # A programmatic way to launch the Celery Beat scheduler.
│       ├── celery-worker.py                    # Celery worker initialization; this uses CreateApp() function defined in app.py
│       └── mailer.py                           # Mail sending utility via Celery; 
├── controller/
│   ├── __init__.py                             # imports and exports send_daily_quiz_reminders, send_monthly_report_to_users from tasks
│   ├── extensions.py                           # Enables security, redis_client, cache, limiter and celery which are imported in app.py
│   ├── models/                                 # All db and ir's models are defined here; Using SQLAlchemy, the ORM
│   │   ├── __init__.py
│   │   ├── chapter_model.py
│   │   ├── enums.py
│   │   ├── question_model.py
│   │   ├── quiz_model.py
│   │   ├── score_model.py
│   │   ├── semester_model.py
│   │   ├── subject_model.py
│   │   └── user_model.py
│   ├── routes/                             
│   │   ├── __init__.py                        # Registers all the APIs
│   │   ├── user.py                            # Defines the API classes used by the users
│   │   ├── auth.py                            # Defines the API classes used for login, logout, register
│   │   └── admin/                             # Defines the API classses used by the admin
|   |       ├── __init__.py
|   |       └── analytics.py                   # Defines the AI classes requied for ChartJS in the front to render the charts
│   ├── tasks/
│   │   ├── __init__.py                        # Importing and exporting the tasks
|   |   ├── README.md                          # Listed things could be added here in the tasks
│   │   ├── send_emails/
│   │   |   ├── __init__.py                    # Importing and exporting the tasks
│   │   |   ├── send_reports.py                # Created a celery task for sending monthly reports to all the active users
│   │   │   ├── send_reminders.py              # created a celery task to send diaily notification of pending quizzes to users
│   │   │   └── html-templates/                # Contains all the HTML templated to be used in the mail
│   │   │       ├── reminder.html
│   │   │       └── report.html
```