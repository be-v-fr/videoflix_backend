=====
SETUP
=====
- Install Redis
- Activate "requirepass" in Redis configuration file
- Create "secret_keys.py" file in project folder and save your Redis password as "REDIS_PW"

========
COMMANDS
========
- Start worker in Windows:
python manage.py rqworker --worker-class videoflix.simpleworker.SimpleWorker default
- Start worker in Linux:
python manage.py rqworker default