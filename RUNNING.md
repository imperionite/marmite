#### 🤖 CLI Commands (DRF)

```bash
# virtual env.
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
$ python manage.py migrate --noinput

# creating super user
python manage.py createsuperuser

# serve backend at localhost:8000
python manage.py runserver

# generating requirements file
pip freeze > requirements.txt

# create secret keys
$ python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
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

<a name="ss"></a>

### 📌 Endpoints and HTTP Request & Response Screenshots

- [HTTP Sample Requests](https://github.com/imperionite/marmite/blob/main/rest.http)

- [HTTP Request & Response Screenshots](https://github.com/imperionite/marmite/blob/main/HTTP.md)

<a name="rl"></a>

### 💻 Running Locally

Make sure you have Docker and openssl package install on your local machine.

Clone the project

```bash
  git clone git@github.com:arnelimperial/connectly.git
```

Generate a self-signed SSL certificate with OpenSSL

```bash
# this will create a folder name ssl at the root of the project
$ mkdir ssl && openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
-out ./ssl/cert.pem -keyout ./ssl/key.pem \
-subj "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=localhost"
```

Create environment variables

```bash
$ cd connectly-api && touch .env

# .env file might look like this one
DEBUG=True
DATABASE_URL=postgres://myuser:mypassword@127.0.0.1:6432/mydatabase
SECRET_KEY=give_me_your_secrets
# optional
GOOGLE_CLIENT_ID=XXXXXXXXXXXXXXXXXXXXXXX
GOOGLE_CLIENT_SECRET=XXXXXXXXXXXXXXXXXXX
```

Install the packages

```bash
# be sure you're in the connectly-api folder and the virtual environment is activated
$ pip install -r requirements.txt
```

Build the services and run Django

```bash
# at the project root
$ cd .. && docker-compose up --build
# run Django server on the other terminal
$ cd connectly-api && python manage.py runserver 0.0.0.0:8000
# this will run at https://127.0.0.1:8080/{what/ever/endpoint/it/is/}
```