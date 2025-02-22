<a name="intro"></a>

# marmite

Refer to the [connectly-api directory](https://github.com/imperionite/marmite/tree/main/connectly-api) for the Django/Django REST API project.

PostgreSQL was utilized as the database for the project, and Nginx was implemented to manage reverse proxying and load balancing. There is a possibility of integrating a frontend service developed in React in the future, primarily for demonstration purposes only. All services (as shown in the System Architecture Diagram) are deployed within Docker containers, except for the [connectly-api project](https://github.com/imperionite/marmite/tree/main/connectly-api), which runs locally on the host machine to simplify usage and avoid issues related to migrations.

The REST API endpoints can be accessed through HTTPS, specifically at localhost https://127.0.0.1:8080/{endpoint}/, since the default Django server port 8000 is being [proxied](https://github.com/imperionite/marmite/blob/main/nginx/nginx.conf).

Certain sensitive `environment variables` are currently made visible; however, their exposure will be minimized in accordance with the project's requirements in the near future.

## 🧬 Table of Contents

1. [ Introduction ](#intro)
2. [ Requisite ](#requisite)
3. [ Initial Data Seeding ](#ids)
4. [ Endpoints and Manual API Tests ](#ss)
5. [ Getting started ](#rl)
6. [ Endpoints ](#ep)
7. [ Security Implemetation](#security)
8. [ Scalability Implemetation](#scalability)
9. [ CLI Commands ](#commands)
10. [ Author ](#author)

<a name="requisite"></a>

### 🤔 Requisite

Basic understanding of Django Stack, Postgres, REST API and web development.

<a name="ids"></a>

## 🧬 Initial Data Seeding

This project utilizes Django fixtures to seed initial data into the database, including users, posts, comments, and likes. This allows for a consistent starting point for development and testing.

### Generating the Fixture Data

The fixture data is generated using a custom Django management command:

1.  Create the `generate_fixture_data.py` file within the `posts/management/commands` directory of your Django app. The contents of this file should be as follows:

    ```python
    # posts/management/commands/generate_fixture_data.py
    import json
    from django.core.management.base import BaseCommand
    from django.contrib.auth.models import User
    from ...models import Post, Comment, Like  # Import your models

    class Command(BaseCommand):
        help = 'Generates fixture data with hashed passwords'

        def handle(self, *args, **options):
            # ... (Code from previous response goes here) ...
    ```

2.  Run the following command to generate the `initial_data.json` file:

    ```bash
    python manage.py generate_fixture_data
    ```

    This command creates the `initial_data.json` file in the `posts/fixtures` directory. It's crucial that this command is run _after_ the initial migrations and _after_ you have created the superuser account (either through `createsuperuser` or within the initial migration itself).

### Loading the Fixture Data

1.  Place the generated `initial_data.json` file in the `posts/fixtures` directory.

2.  Load the fixture data into the database using the following command:

    ```bash
    python manage.py loaddata posts/fixtures/initial_data.json
    ```

### Fixture Data Details

The `initial_data.json` file contains the following data:

- **Users:** 5 users are created, including one superuser (admin) and four regular users. Usernames and emails are in the format `user0`, `user1`, etc. The password for all users is `passworD1#` (hashed using Django's password hashing).
- **Posts:** 6 posts are created, authored by different users.
- **Comments:** 5 comments are created, associated with specific posts and users.
- **Likes:** 3 likes are created, associating users with posts.
- **Unlikes:** 2 "unlikes" are simulated by creating likes that you would then delete if you were implementing unliking functionality. This is how you represent the "unlike" state in a fixture.

### Important Considerations

- **Password Hashing:** The `generate_fixture_data` command handles password hashing securely using Django's built-in methods. **Do not** attempt to store plain text passwords in your fixtures.
- **Dependencies:** The order of objects in the JSON file is important due to foreign key constraints. Users must be created before posts, posts before comments and likes, and so on. The provided command handles this automatically.
- **Running Order:** Ensure that you run the `generate_fixture_data` command _after_ running your initial migrations (`python manage.py migrate`) and _after_ creating the superuser account. The superuser should be created either through `createsuperuser` or within the initial migration itself. Then, run `loaddata`.

<a name="ep"></a>

## Endpoints

### User

**Public Endpoints:**

- **POST /posts/users/** – Create a new user.

**Protected Endpoints (Authentication Required):**

- **GET /posts/users/** – List all users.
- **GET /posts/users/{id}/** – Retrieve a specific user.

**Protected Endpoints (Authentication + Authorization Required):**

- **PUT /posts/users/{id}/** – Update a specific user.
- **PATCH /posts/users/{id}/** – Partially update a specific user.
- **DELETE /posts/users/{id}/** – Delete a specific user.

All `User` endpoints are now secured with appropriate permissions ensuring public access only for registration and authenticated/authorized access for all other actions.

### Post

### **Public Endpoints:**

- **GET /posts/** – List all posts.
- **GET /posts/{id}/** – Retrieve a specific post.

### **Protected Endpoints (Authentication Required):**

- **POST /posts/** – Create a new post (only authenticated users can create posts).
- **GET /posts/{id}/comments/** – List all comments on a specific post with pagination.
- **POST /posts/{id}/like/** – Like a specific post.
- **DELETE /posts/{id}/unlike/** – Unlike a specific post.

### **Protected Endpoints (Authentication + Authorization Required):**

- **PUT /posts/{id}/** – Update a specific post (only the author of the post can update).
- **PATCH /posts/{id}/** – Partially update a specific post (only the author can update).
- **DELETE /posts/{id}/** – Delete a specific post (only the author can delete).

### Comment

**Public Endpoints:**

- **GET /posts/comments/** – List all comments.
- **GET /posts/comments/{id}/** – Retrieve a specific comment.

**Protected Endpoints (Authentication Required):**

- **POST /posts/comments/** – Create a new comment (only authenticated users can create comments).

**Protected Endpoints (Authentication + Authorization Required):**

- **PUT /posts/comments/{id}/** – Update a specific comment (only the comment's author can update).
- **PATCH /posts/comments/{id}/** – Partially update a specific comment (only the comment's author can update).
- **DELETE /posts/comments/{id}/** – Delete a specific comment (only the comment's author can delete).

This implementation ensures that comment-related operations are secured, allowing only authenticated users to create comments and only the comment author to update or delete their comments.

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

<a name="commands"></a>

#### 🤖 CLI Commands

Refer to [RUNNING.md](https://github.com/imperionite/marmite/tree/main/RUNNING.md) file for details on the commonly use commads in the project.

<a name="author"></a>

### 👨🏻‍💻 Author

- [Arnel Imperial](https://github.com/imperionite)
