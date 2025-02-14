<a name="intro"></a>

# marmite

Refer to the [connectly-api directory](https://github.com/imperionite/marmite/tree/main/connectly-api) for the Django/Django REST API project.

PostgreSQL was utilized as the database for the project, and Nginx was implemented to manage reverse proxying and load balancing. There is a possibility of integrating a frontend service developed in React in the future, primarily for demonstration purposes only. All services (as shown in the System Architecture Diagram) are deployed within Docker containers, except for the [connectly-api project](https://github.com/imperionite/marmite/tree/main/connectly-api), which runs locally on the host machine to simplify usage and avoid issues related to migrations.

The REST API endpoints can be accessed through HTTPS, specifically at localhost https://127.0.0.1:8080/{endpoint}/, since the default Django server port 8000 is being [proxied](https://github.com/imperionite/marmite/blob/main/nginx/nginx.conf).

Certain sensitive `environment variables` are currently made visible; however, their exposure will be minimized in accordance with the project's requirements in the near future.

**General notes on my implementation for all CRUD operations (CREATE, READ, UPDATE, DELETE):**

When using a ModelViewSet, it inherently supports all CRUD (Create, Read, Update, Delete) operations by default. This means that without explicitly writing code for each action (like PUT, PATCH, or DELETE), these actions are still available and functional.

For example:

- **Update Operations**: Both **full updates (PUT)** and **partial updates (PATCH)** are handled by the `.update()` and `.partial_update()` methods respectively.
- **Delete Operations**: The `.destroy()` method handles deletions.

Here’s how these actions map to HTTP methods:

- GET (Retrieve): Supported via .retrieve() method.
- POST (Create): Supported via .create() method.
- PUT/PATCH (Update): Supported via .update()/.partial_update() methods respectively.
- DELETE (Delete): Supported via .destroy() method

The implementation using ModelViewSet and the router (DefaultRouter or SimpleRouter) in Django REST Framework does automatically include the ID in the URL for update and delete operations.

When registered a viewset with a router like this:

```py
router.register(r'users', UserViewSet, basename='user')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')
```

The resulting URLs will be structured as follows:

```bash
Retrieve (GET): /users/{id}/
Update (PUT/PATCH): /users/{id}/
Delete: /users/{id}/
```

Similarly for posts and comments:

```bash
Retrieve (GET): /posts/{id}/, /comments/{id}/
Update (PUT/PATCH): /posts/{id}/, /comments/{id}/
Delete: /posts/{id}/, /comments/{id}/
```

## 🧬 Table of Contents

1. [ Introduction ](#intro)
2. [ Requisite ](#requisite)
3. [ CLI Commands ](#commands)
4. [ Endpoints and HTTP Request & Response Screenshots ](#ss)
5. [ Running Locally ](#rl)
6. [ Author ](#author)

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

<a name="author"></a>

### 👨🏻‍💻 Author

- [Arnel Imperial](https://github.com/imperionite)