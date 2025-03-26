#### 🤖 CLI Commands (DRF)

```bash
## delete and re-create new virtual env if environment is not detected by VS Code
# reinstall the packages again
$ python -m venv .venv # create
$ source .venv/bin/activate # activate
$ deactivate # deactivate

# install dependencies (backend)
pip install dependency_name

# creating backend project
django-admin startproject core .

# creating backend local apps
python manage.py startapp app_name

# create and apply migration
$ python manage.py makemigrations --dry-run --verbosity 3 # dry-run
$ python manage.py makemigrations
$ python manage.py migrate --no-input

# creating super user
python manage.py createsuperuser
# create superuser in command base
python manage.py create_superuser

# serve backend at localhost:8000
python manage.py runserver

# generating requirements file
pip freeze > requirements.txt

# create secret keys
$ python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# running fixture, for initial run only, when flush DB or on intial deployment setup, 
# just delete first the initial_data.json in fixtures directory to generate new one
python connectly-api/manage.py generate_fixture_data 
# python connectly-api/manage.py loaddata connectly-api/posts/fixtures/initial_data.json

# assign roles to seeded user data
python connectly-api/manage.py assign_roles

# remove all records from the entire database (including resetting auto-incrementing primary keys)
python connectly-api/manage.py flush

# Render start command
gunicorn --pythonpath connectly-api --workers 3 --bind 0.0.0.0:$PORT core.wsgi:application

# Render build command
./build.sh

# ensure excution permission on all .sh files
chmod +x SH/build_debug.sh # for DRF debug
chmod +x SH/build.sh # for render.com
chmod +x K6/run_k6_tests.sh # for K6 load testing

./SH/build.sh # run the script on render
./SH/build_debug.sh # run to build DRF on debug mode
./K6/run_k6_tests.sh # run to automate the K6 load testing


# https://marmite.onrender.com


# postgres
docker ps
docker exec -it [postgres_container_id] bash
psql -U myuser mydatabase
\! clear # clear screen
\dt # list tables
\dt public.* # list all tables in public schema
\dt * # list tables from all schema
\dt posts_user # specific table
SELECT * FROM posts_user;
SELECT id, username, email, password, created_at, date_joined, is_staff FROM posts_user;
\q # quit psql

# redis
docker ps
docker exec -it <redis_container_name> redis-cli
```


#### 🤖 CLI Commands (Docker)

```bash
# create Docker Network
$ docker network create app-network
$ docker network ls

# build & run containers on detached mode
$ docker-compose up --build -d

# stop running container and remove volumes
$ docker-compose down -v

# clean slate
$ docker system prune -a && docker images prune -a && docker volume prune -a
```

