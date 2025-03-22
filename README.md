<a name="intro"></a>

# marmite

Refer to the [connectly-api directory](https://github.com/imperionite/marmite/tree/main/connectly-api) for the Django/Django REST API project.

**PostgreSQL** was utilized as the database for the project, and Nginx was implemented to manage reverse proxying and load balancing. There is a possibility of integrating a frontend service developed in React in the future, primarily for demonstration purposes only. All services (as shown in the System Architecture Diagram) are deployed within Docker containers, except for the [connectly-api project](https://github.com/imperionite/marmite/tree/main/connectly-api), which runs locally on the host machine to simplify usage and avoid issues related to migrations.

The data schema is defined using Django's ORM (Object-Relational Mapper). Key models include:

- **User:** Represents a user of the system, extending Django's built-in User model to include additional fields like `email` and `created_at`. Authentication and authorization are handled using Django's authentication framework, with JWT (JSON Web Tokens) for API authentication.
- **Post:** Stores the content of a post, authored by a User.
- **Comment:** Stores a comment on a Post, authored by a User.
- **Like:** Represents a "like" on a Post by a User. A unique constraint prevents duplicate likes from the same user on the same post.

The relationships between these models are defined using ForeignKey relationships in Django. For example, a Post has a ForeignKey to the User who authored it. This allows for efficient querying and retrieval of related data.

Data migrations are used to manage database schema changes over time. Migrations are Python scripts that define how to create, alter, or delete database tables and fields. This ensures that the database schema is always consistent with the application's models.

Initial data, such as a set of users, posts, comments, and likes, can be seeded into the database using Django fixtures. This is helpful for development, testing, and ensuring a consistent starting point for the application. A custom Django management command is used to generate the fixture data, including properly hashed user passwords.

The REST API endpoints can be accessed through HTTPS, specifically at localhost https://127.0.0.1:8080/{endpoint}/, since the default Django server port 8000 is being [proxied](https://github.com/imperionite/marmite/blob/main/nginx/nginx.conf).

Certain sensitive `environment variables` are currently made visible; however, their exposure will be minimized in accordance with the project's requirements in the near future.

## 🧬 Table of Contents

1. [ Introduction ](#intro)
2. [ Requisite ](#requisite)
3. [ Initial Data Seeding ](#ids)
4. [ Endpoints ](#ep)
5. [ Manual API Tests ](#ss)
6. [ Getting started ](#rl)
7. [ Security Implemetation](#security)
8. [ Scalability Implemetation](#scalability)
9. [ CLI Commands ](#commands)
10. [ Diagrams ](#diagrams)
11. [ Author ](#author)

<a name="requisite"></a>

### 🤔 Requisite

Basic understanding of Django Stack, Postgres, REST API and web development.

<a name="ids"></a>

## 🌱 Initial Data Seeding

This project employs a combined approach to API testing, leveraging both manual testing with REST Client (a VS Code extension) and the use of [Django data fixtures](https://docs.djangoproject.com/en/5.1/topics/db/fixtures/) for efficient database initialization. The objective is to ensure comprehensive validation of the API endpoints while maintaining a streamlined development workflow.

Specifically, Django data fixtures are used to seed the database with initial data, including users, posts, comments, and likes. This practice provides a consistent and predictable foundation for testing and development, ensuring that all team members and automated processes operate from the same baseline data state. The fixture implementation directly supports the project's goal of creating a robust and reliable API.

Manual API testing, performed using REST Client, serves as a critical component of the overall testing strategy. REST Client allows for direct interaction with the API endpoints, enabling detailed inspection of request/response cycles and providing a means to validate both expected and edge-case scenarios. The results of these manual tests are meticulously documented in [USERS_HTTP.md](https://github.com/imperionite/marmite/blob/main/USERS_HTTP.md), [POSTS_HTTP.md](https://github.com/imperionite/marmite/blob/main/POSTS_HTTP.md) and [COMMENTS_HTTP.md](https://github.com/imperionite/marmite/blob/main/COMMENTS_HTTP.md). These files contain detailed request examples, corresponding responses, and supporting screenshots that capture the state of the application during various test executions.

**Detailed Explanation of Screenshot Data & the Role of Fixtures:**

To provide full transparency, it's crucial to clarify the relationship between the data presented in the REST Client screenshots and the data now generated by the Django fixtures. While I am committed to maintaining accurate and up-to-date documentation, certain factors necessitate a nuanced understanding of these resources:

- **Demonstrating Manual API Proficiency:** A primary goal of the REST Client documentation is to demonstrate proficiency in manual API testing techniques. The included `.http` files and associated screenshots provide concrete evidence that I have diligently exercised the API endpoints and validated their functionality according to the project's requirements. This initial phase of manual testing was essential for understanding the API's behavior and identifying potential areas for improvement.
- **Temporal Discrepancy: Screenshots vs. Fixtures:** A significant portion of the screenshots within the `USERS_HTTP.md`, `POSTS_HTTP.md`, and `COMMENTS_HTTP.md` files were captured _prior_ to the final implementation and integration of Django data fixtures. As a result, the data displayed in these earlier screenshots may _not_ precisely reflect the data currently populated by the fixtures. This discrepancy is purely temporal and stems from the iterative nature of the development process.
- **Core API Functionality: The Constant Factor:** It's imperative to emphasize that the _underlying functionality_ of the API endpoints remains constant and unaffected by the specific data being used. The manual tests documented in the HTTP files accurately validate the API's ability to handle requests, process data, and return appropriate responses, regardless of whether the data originates from manual input or from the fixtures. The focus is on the correct operation of the _endpoints themselves_.
- **Current Testing Practices: Fixture-Aware Screenshots:** All _new_ manual API tests, performed after the integration of Django data fixtures, will include screenshots that explicitly showcase the data generated by the fixtures. This ensures that future documentation accurately reflects the current state of the application and provides a consistent view of the data being used during testing.
- **Justification for Retaining Existing Screenshots: Avoiding Redundant Effort:** The decision to retain the existing screenshots, despite the potential data mismatch, is based on a pragmatic assessment of the effort required to re-capture all test cases. Given that the core API functionality has already been thoroughly validated through manual testing, re-performing all tests solely for the purpose of updating the screenshots would represent a significant and unjustifiable investment of time and resources. The existing screenshots serve as valuable historical documentation of the testing process and demonstrate the evolution of the project.
- **Comprehensive Testing Coverage: A Holistic View:** By presenting both the initial manual testing results and the subsequent fixture-based approach, I aim to provide a comprehensive and holistic view of the testing strategy employed in this project. This approach ensures that all aspects of the API have been rigorously validated, from the initial exploration of individual endpoints to the automated seeding of consistent data for ongoing development and testing.

### Sample Initial Data in the DB

#### All Initial Public Tables

![public tables](https://drive.google.com/uc?id=1waXZDtu8Et_4kNX210ujx_sepgEK7DtP)

#### User Table

![user table](https://drive.google.com/uc?id=1I45Bhfrlg9x5BXvDUskIKj3oHtLaLJln)

#### Initial Post Table

![post table](https://drive.google.com/uc?id=1iwB4TQJwF_2DGEMgga_lOYFCsJy5NBYO)

#### Initial Comment Table

![comment table](https://drive.google.com/uc?id=1rlJ-h2_VmCzbyiFrGEqrUE-Oq2czd9YU)

#### Initial Like Table

![like table](https://drive.google.com/uc?id=19wVsnd6rCrsYqhgRwkVqw9O_GZzFqLMl)

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

2.  Run the following command to generate the `initial_data.json` file, ensure that `fixtures` directory has already been created inside the `posts` app directory:

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
- **Running Order:** Ensure that you run the `generate_fixture_data` command _after_ running your initial migrations (`python manage.py migrate`) and _after_ creating the superuser account. The superuser should be created either through `createsuperuser` or within the initial migration itself. Then, run `python connectly-api/manage.py generate_fixture_data` and `python connectly-api/manage.py assign_roles` to assigned user role.

<a name="ep"></a>

## 📌 Endpoints

| **Category** | **Endpoint**           | **Method** | **Description**             | **Auth Required** | **Access Level**    |
| ------------ | ---------------------- | ---------- | --------------------------- | ----------------- | ------------------- |
| **Users**    | `/users/`              | `GET`      | List all users              | Yes               | Admin only          |
|              | `/users/`              | `POST`     | Create a new user           | No                | Public              |
|              | `/users/{id}/`         | `GET`      | Retrieve a specific user    | Yes               | Owner or Admin      |
|              | `/users/{id}/`         | `PUT`      | Update a specific user      | Yes               | Owner or Admin      |
|              | `/users/{id}/`         | `PATCH`    | Partially update a user     | Yes               | Owner or Admin      |
|              | `/users/{id}/`         | `DELETE`   | Delete a specific user      | Yes               | Owner or Admin      |
| **Posts**    | `/posts/`              | `GET`      | List all posts              | No                | Public              |
|              | `/posts/`              | `POST`     | Create a new post           | Yes               | Authenticated users |
|              | `/posts/{id}/`         | `GET`      | Retrieve a specific post    | No                | Public              |
|              | `/posts/{id}/`         | `PUT`      | Update a specific post      | Yes               | Owner or Admin      |
|              | `/posts/{id}/`         | `PATCH`    | Partially update a post     | Yes               | Owner or Admin      |
|              | `/posts/{id}/`         | `DELETE`   | Delete a specific post      | Yes               | Owner or Admin      |
|              | `/posts/{id}/like/`    | `POST`     | Like a specific post        | Yes               | Authenticated users |
|              | `/posts/{id}/unlike/`  | `POST`     | Unlike a specific post      | Yes               | Authenticated users |
|              | `/posts/{id}/comment/` | `POST`     | Add a comment to a post     | Yes               | Authenticated users |
| **Comments** | `/comments/`           | `GET`      | List all comments           | No                | Public              |
|              | `/comments/`           | `POST`     | Create a new comment        | Yes               | Authenticated users |
|              | `/comments/{id}/`      | `GET`      | Retrieve a specific comment | No                | Public              |
|              | `/comments/{id}/`      | `PUT`      | Update a specific comment   | Yes               | Owner or Admin      |
|              | `/comments/{id}/`      | `PATCH`    | Partially update a comment  | Yes               | Owner or Admin      |
|              | `/comments/{id}/`      | `DELETE`   | Delete a specific comment   | Yes               | Owner or Admin      |

<a name="ss"></a>

## 🧪 Manual API Tests

| Category | Description                                                                                                      | Documentation                                                                 | API Calls Collection                                                                 |
| -------- | ---------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Users    | Endpoints related to user authentication, registration, and management.                                          | [Users](https://github.com/imperionite/marmite/blob/main/USERS_HTTP.md)       | [Users API Calls](https://github.com/imperionite/marmite/blob/main/users.http)       |
| Posts    | Endpoints for creating, retrieving, updating, and deleting posts. Includes interactions like likes and comments. | [Posts](https://github.com/imperionite/marmite/blob/main/POSTS_HTTP.md)       | [Posts API Calls](https://github.com/imperionite/marmite/blob/main/posts.http)       |
| Comments | Endpoints to manage comments on posts, including adding, retrieving, updating, and deleting comments.            | [Comments](https://github.com/imperionite/marmite/blob/main/COMMENTS_HTTP.md) | [Comments API Calls](https://github.com/imperionite/marmite/blob/main/comments.http) |

<a name="rl"></a>

## 💻 Running Locally

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

## ⛑️ Current Security Implementation

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

## 🏗️ Current Scalability Implementation

Our project is designed with scalability in mind, incorporating several key features that enhance its ability to handle increased load and provide a reliable user experience:

1. **Load Balancing with Nginx**: We utilize Nginx as a reverse proxy to distribute incoming requests across multiple instances of our Django application, improving throughput and fault tolerance.

2. **Docker Containerization**: The application components are containerized using Docker, ensuring consistent environments and simplifying scaling by adjusting container counts as needed.

3. **Database Connection Pooling with PgBouncer**: PgBouncer manages database connections efficiently, reducing overhead and improving performance during high-load scenarios.

4. **Horizontal Scaling Potential**: The architecture supports horizontal scaling by allowing additional instances of both the Django application and PostgreSQL database to be added easily.

5. **Docker Compose for Service Management**: We leverage Docker Compose for defining and managing our multi-container application stack, simplifying deployment and inter-service communication.

These features collectively contribute to a robust and scalable architecture capable of accommodating future growth.

<a name="commands"></a>

## 🤖 CLI Commands

Refer to [RUNNING.md](https://github.com/imperionite/marmite/tree/main/RUNNING.md) file for details on the commonly use commads in the project.

<a name="diagrams"></a>

## 🔗 Diagrams

Refer to this [link](https://github.com/imperionite/marmite/tree/main/DIAGRAMS.md) for the diagrams in the project.

<a name="author"></a>

### 👨🏻‍💻 Author

- [Arnel Imperial](https://github.com/imperionite)
