System setup
============
- Install PostgreSQL
- Install FFMPEG
- Install Redis
- Activate "requirepass" in Redis configuration file
- Create "secret_keys.py" file in project folder and save your Redis password as "REDIS_PW"

Postgres setup
==============
- Switch to postgres user in bash: "sudo su postgres"
- Add "DB_ADMIN_NAME" and "DB_ADMIN_PW" to "secret_keys.py"
- Create DB (in the following command, replace [DB_ADMIN_NAME] and [DB_ADMIN_PW] with their respective values, leaving aside the brackets):

psql -c "CREATE DATABASE videoflix"
psql -c "CREATE USER [DB_ADMIN_NAME] WITH PASSWORD '[DB_ADMIN_PW]'"
psql -d videoflix -c "CREATE SCHEMA public AUTHORIZATION [DB_ADMIN_NAME]"
psql -c "ALTER ROLE [DB_ADMIN_NAME] SET client_encoding TO 'utf8'"
psql -c "ALTER ROLE [DB_ADMIN_NAME] SET default_transaction_isolation TO 'read committed'"
psql -c "ALTER ROLE [DB_ADMIN_NAME] SET timezone TO 'UTC'"
psql -c "GRANT ALL PRIVILEGES ON SCHEMA public TO [DB_ADMIN_NAME];"
psql -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO [DB_ADMIN_NAME];"

Commands
========
- Start worker in Windows:
python manage.py rqworker --worker-class videoflix.simpleworker.SimpleWorker default
- Start worker in Linux:
python manage.py rqworker default