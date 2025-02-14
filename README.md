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
6.  [Security Implemetation](#security)
7.  [Scalability Implemetation](#scalability)
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


<a name="security"></a>

## Current Security Implementation

In our project, we have implemented a comprehensive security architecture to safeguard user data and ensure secure communication. The following components highlight our security measures:

### 1. HTTPS Configuration

To protect data in transit, we have configured Nginx to serve our application over HTTPS. This is accomplished using a self-signed SSL certificate generated with OpenSSL. The SSL certificate and key are securely mounted within the Nginx container, enabling encrypted connections on port 8080.

### 2. Django Security Settings

Our Django application is configured with several critical security settings:

- **Secret Key Management**: The `SECRET_KEY` is stored as an environment variable, preventing exposure in the source code.
- **Debug Mode**: The `DEBUG` setting is disabled in production environments to prevent sensitive information from being displayed in error messages.
- **Allowed Hosts**: The `ALLOWED_HOSTS` setting restricts which host/domain names can serve the application, mitigating HTTP Host header attacks.

### 3. Middleware for Security

We utilize Django's built-in middleware to enhance application security:

- **Security Middleware**: This middleware adds several security-related HTTP headers to responses.
- **CSRF Protection**: Cross-Site Request Forgery protection is enabled by default through the `CsrfViewMiddleware`, ensuring that state-changing requests are verified.
- **XFrameOptions Middleware**: This middleware prevents clickjacking by controlling whether your site can be embedded in an iframe.

### 4. CORS Configuration

Cross-Origin Resource Sharing (CORS) is configured to restrict which domains can access our API:

- **CORS Origin Whitelist**: We specify allowed origins to enhance security while allowing legitimate requests.
- **CORS Credentials**: The setting allows cookies and authentication headers to be sent with cross-origin requests.

### 5. Authentication and Permissions

We implement robust authentication and authorization mechanisms:

- **JWT Authentication**: We use JSON Web Tokens (JWT) for secure user authentication via the `rest_framework_simplejwt` library, allowing for stateless sessions.
- **Custom Permissions**: Custom permission classes (`IsAdmin`, `IsPostAuthor`) are defined to control access to specific views based on user roles and ownership.

### 6. Password Management

To ensure strong password security, we employ multiple password hashing algorithms, including Argon2 and BCryptSHA256. Additionally, we enforce password validation rules that require minimum length and complexity.

### 7. Secure Cookies

We configure session and CSRF cookies with security attributes:

- **Secure Cookies**: Cookies are set to be secure and HTTP-only, preventing them from being accessed via JavaScript.
- **SameSite Attribute**: CSRF cookies are configured with the `SameSite` attribute to mitigate CSRF attacks.

### 8. HSTS Configuration

HTTP Strict Transport Security (HSTS) is enabled to enforce secure connections:

- **HSTS Settings**: We specify a long duration for HSTS (1 year) and include subdomains, ensuring that all communications are conducted over HTTPS.

### Security Practices and Incident Remediation

#### OpenSSL Keys and Certificates Management

As part of our project's security implementation, we use OpenSSL to generate SSL certificates for secure HTTPS communication. However, during development, an oversight led to the accidental exposure of private keys and certificates in the public repository. This was promptly detected by GitGuardian, a tool we use for automated secrets detection.

To remediate this issue and prevent future occurrences:

1. **Immediate Action Taken**:
   - The exposed keys and certificates were immediately revoked and replaced with new ones.
   - All related commits were removed from the repository's history to ensure the sensitive data is no longer accessible.

2. **Preventive Measures**:
   - The `ssl` directory containing keys and certificates has been added to the `.gitignore` file to prevent accidental inclusion in future commits.
   - We have integrated GitGuardian into our development workflow to continuously monitor for exposed secrets in real-time.

3. **Best Practices Moving Forward**:
   - Sensitive files, such as private keys and certificates, will be stored securely outside the repository.
   - Environment variables will be used to manage sensitive configurations wherever applicable.
   - Regular audits will be conducted to ensure compliance with security best practices.

By addressing this incident transparently and implementing robust preventive measures, we aim to uphold the highest standards of security in our project.


<a name="scalability"></a>

## Current Scalability Implementation

Our project is designed with scalability in mind, incorporating several key features that enhance its ability to handle increased load and provide a reliable user experience:

1. **Load Balancing with Nginx**: We utilize Nginx as a reverse proxy to distribute incoming requests across multiple instances of our Django application, improving throughput and fault tolerance.

2. **Docker Containerization**: The application components are containerized using Docker, ensuring consistent environments and simplifying scaling by adjusting container counts as needed.

3. **Database Connection Pooling with PgBouncer**: PgBouncer manages database connections efficiently, reducing overhead and improving performance during high-load scenarios.

4. **Horizontal Scaling Potential**: The architecture supports horizontal scaling by allowing additional instances of both the Django application and PostgreSQL database to be added easily.

5. **Docker Compose for Service Management**: We leverage Docker Compose for defining and managing our multi-container application stack, simplifying deployment and inter-service communication.

These features collectively contribute to a robust and scalable architecture capable of accommodating future growth.


<a name="author"></a>

### 👨🏻‍💻 Author

- [Arnel Imperial](https://github.com/imperionite)