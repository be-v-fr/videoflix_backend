Videoflix (backend) is a Django backend providing a video streaming platform.
The platform provides
- an API
- automatic conversion of video uploads to HLS/streaming format.

(c) 2025 Bengt Früchtenicht

System setup
============
- Execute `pip install -r requirements.txt`
- Install PostgreSQL
- Install FFMPEG
- Install Redis
- Create `secret_keys.py` file in project folder

Redis configuration
===================
- Activate `requirepass` in Redis configuration file
- Save your Redis password as `REDIS_PW` in `secret_keys.py`

Postgres setup
==============
- Switch to postgres user in bash: `sudo su postgres`
- Add `DB_ADMIN_NAME` and `DB_ADMIN_PW` to `secret_keys.py`
- Create database (in the following commands, replace `DB_ADMIN_NAME` and `DB_ADMIN_PW` with their respective values):

`psql -c "CREATE DATABASE videoflix"`\
`psql -c "CREATE USER DB_ADMIN_NAME WITH PASSWORD 'DB_ADMIN_PW'"`\
`psql -d videoflix -c "CREATE SCHEMA public AUTHORIZATION DB_ADMIN_NAME"`\
(in case the schema "public" already exists:\
`psql -d videoflix -c "ALTER SCHEMA public OWNER TO DB_ADMIN_NAME;"`)\
`psql -c "ALTER ROLE DB_ADMIN_NAME SET client_encoding TO 'utf8'"`\
`psql -c "ALTER ROLE DB_ADMIN_NAME SET default_transaction_isolation TO 'read committed'"`\
`psql -c "ALTER ROLE DB_ADMIN_NAME SET timezone TO 'UTC'"`\
`psql -c "GRANT ALL PRIVILEGES ON SCHEMA public TO DB_ADMIN_NAME;"`\
`psql -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO DB_ADMIN_NAME;"`

- And to allow creating a test database when running automatic tests:

`psql -c "ALTER USER DB_ADMIN_NAME CREATEDB;"`

Setup email backend
===================
- The backend is configured to use SMTP (Simple Mail Transfer Protocol).
- To use this configuration, please add
    - `EMAIL_HOST` (your email server URL),
    - `EMAIL_USER` (your email sender username) and
    - `EMAIL_PASSWORD` (the sender's correct password)
  
  to `secret_keys.py`.
- For development purposes, you can replace the `EMAIL_BACKEND` value with `"django.core.mail.backends.console.EmailBackend"`. That way, the backend will simply show the email content in the console instead of sending an actual email. This will not require any further configuration.

Django setup
============
- Add a `DJANGO_SECRET_KEY` to `secret_keys.py` to set the `settings.SECRET_KEY` property.
    - You can generate a key over here: https://djecrety.ir/

Content setup
=============
- Upload videos using the Django admin interface while running a worker in addition to the Django server.
- If you use the Videoflix frontend repo: Create a guest user using
    - an arbitrary username,
    - the email `guest@videoflix.com` and
    - the password `gu3stl0g1n`.

Basic commands
==============
- Start worker in Linux:\
`python manage.py rqworker default`
- Start worker in Windows:\
`python manage.py rqworker --worker-class videoflix.simpleworker.SimpleWorker default`
- Run Django server:\
`python manage.py runserver`

Test coverage
=============
- To measure test coverage, run `coverage run manage.py test`.
- To report the test coverage, run `coverage report`.

Documentation
=============
- The documentation is stored in `docs_app/docs/_build/html`.
- There are at least three ways to access it:
    - Using the Django server, the documentation can be found under the `/docs` URL. 
    - Using `index.html`, the documentation can be hosted itself.
    - Locally, the documentation can be accessed through the file explorer directly.