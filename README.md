<a name="intro"></a>

# connectly

Refer to the [connectly-api directory](https://github.com/arnelimperial/connectly/tree/main/connectly-api) for the Django/Django REST API project.

PostgreSQL was utilized as the database for the project, and Nginx was implemented to manage reverse proxying and load balancing. There is a possibility of integrating a frontend service developed in React in the future, primarily for demonstration purposes only. All services (as shown in the System Architecture Diagram) are deployed within Docker containers, except for the [connectly-api project](https://github.com/arnelimperial/connectly/tree/main/connectly-api), which runs locally on the host machine to simplify usage and avoid issues related to migrations. 

The REST API endpoints can be accessed through HTTPS, specifically at localhost https://127.0.0.1:8080/{endpoint}/, since the default Django server port 8000 is being [proxied](https://github.com/arnelimperial/connectly/blob/main/nginx/nginx.conf).

Certain sensitive `environment variables` are currently made visible; however, their exposure will be minimized in accordance with the project's requirements in the near future.

## 🧬 Table of Contents

1. [ Introduction ](#intro)
2. [ Requisite ](#requisite)
4. [ CLI Commands ](#commands)
5. [ Basic System Architecture Diagram ](#diagram)
6. [ Endpoints and HTTP Request & Response Screenshots ](#ss)
7. [ Running Locally ](#rl)
8. [ Author ](#author)

<a name="requisite"></a>

### 🤔 Requisite

Basic understanding of Django Stack, Postgres, REST API and web development.


<a name="commands"></a>


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
$ python manage.py migrate --noiinput

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


<a name="diagram"></a>

### 🔗 System Architecture Diagram

![System architecture diagram](https://drive.google.com/uc?id=1W9vta3B3OZl48e0kVfaOzcS0ITPIoZ-Z)


<a name="ss"></a>

### 📌 Endpoints and HTTP Request & Response Screenshots

- [HTTP Sample Requests](https://github.com/arnelimperial/connectly/blob/main/rest.http)

- [HTTP Request & Response Screenshots](https://github.com/arnelimperial/connectly/blob/main/HTTP.md)



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


<a name="author"></a>


### 👨🏻‍💻 Author

- [Arnel Imperial](https://github.com/arnelimperial)

