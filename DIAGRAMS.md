## Diagrams

## Homework 6: Integrating Third-Party Services

**1. Authentication and Authorization Flow Diagram**

![Authentication and Authorization Flow](https://drive.google.com/uc?id=1PaEmp7Y7E0wcPsBMJmGWJdNwMz0iPwYY)

- **Initiate Google Login:**

  - The user, through the React frontend, initiates the Google login process.
  - This action redirects the user to Google's OAuth 2.0 authorization server.

- **Google ID Token:**

  - Upon successful authentication with Google, Google's server returns an ID token to the React frontend.
  - This token contains user information and serves as proof of authentication.

- **POST /api/auth/social/google/:**

  - The React frontend sends a POST request to the backend's `/api/auth/social/google/` endpoint.
  - This request includes the Google ID token in the request body.

- **Verify ID Token:**

  - The Django/DRF backend receives the ID token and sends it to Google's verification service.
  - This step ensures the token's authenticity and validity.

- **Verification Result:**

  - Google's verification service returns a result to the backend, indicating whether the token is valid or invalid.

- **Token Valid (Conditional):**

  - If the token is valid, the backend proceeds with the following steps:
    - **Check Social Account:**
      - The backend queries the database to check if a social account associated with the Google user ID already exists.
    - **Social Account Exists/Not Exists (Conditional):**
      - **Social Account Exists:**
        - If the social account exists, the backend retrieves the corresponding user data from the database.
      - **Social Account Does Not Exist:**
        - If the social account does not exist, the backend requests user information from Google.
        - The backend then creates a new user and a new social account record in the database.
    - **Update/Create Social Login:**
      - The backend updates or creates a social login entry in the database, linking the social account to the user.
    - **Generate JWT Token:**
      - The backend generates a JSON Web Token (JWT), containing access and refresh tokens.

- **JWT Token:**

  - The backend sends the generated JWT token to the React frontend.

- **Store JWT Token:**

  - The React frontend stores the JWT token for subsequent API requests.

- **Protected API Request:**

  - The React frontend makes a request to a protected API endpoint, including the JWT token in the Authorization header.

- **Validate JWT Token:**

  - The Django/DRF backend receives the request and validates the JWT token.

- **Token Valid (Conditional):**

  - If the JWT token is valid:
    - **Fetch Resource:**
      - The backend retrieves the requested resource from the database.
    - **Resource Data:**
      - The backend sends the resource data to the React frontend.

- **Token Invalid (Conditional):**
  - If either the Google ID token or the JWT token is invalid, the backend returns an error response to the React frontend.

---

## Homework 5: Adding User Interactions (Likes and Comments)

**1. Data Relationship Diagram**

![Data Relationship](https://drive.google.com/uc?id=1AgKyroM7R5oaeaTcnFAc8ectJk9gT1M4)

This diagram illustrates the structure and relationships between your core models: `User`, `Post`, `Comment`, and `Like`. Here’s a breakdown:

- **User ↔ Post:**  
  A one-to-many relationship — a single `User` can create multiple `Posts` (`author` field).
- **User ↔ Comment:**  
  Another one-to-many relationship — a `User` can write multiple `Comments` (`user` field).
- **Post ↔ Comment:**  
  A one-to-many relationship — a `Post` can have many `Comments` (`post` field).
- **User ↔ Like:**  
  A one-to-many relationship — a `User` can like multiple `Posts`, but only once per post (enforced by `unique_together`).
- **Post ↔ Like:**  
  A one-to-many relationship — a `Post` can receive many `Likes` from different users.

This diagram reflects how data is stored and linked in the API. When creating views and serializers, understanding these relationships makes it easier to structure queries, permissions, and validations efficiently.

---

**2. CRUD Interaction Flow Diagram**

![CRUD Interaction Flow](https://drive.google.com/uc?id=1_ljXYK0j7xOl5aVoXKGngc-rnKHSLk_o)

This shows how different API endpoints enable CRUD (Create, Read, Update, Delete) operations on the resources — `User`, `Post`, `Comment`, and `Like`. It reflects your RESTful API design:

- **Users:**

  - `POST /users/` — Create a user
  - `POST /users/login/` — User login
  - `GET /users/{id}/` — Retrieve a specific user
  - `PUT /users/{id}/` — Update user details
  - `DELETE /users/{id}/` — Delete a user

- **Posts:**

  - `POST /posts/` — Create a post
  - `GET /posts/` — List all posts
  - `GET /posts/{id}/` — Retrieve a specific post
  - `PUT /posts/{id}/` — Update a post
  - `DELETE /posts/{id}/` — Delete a post

- **Comments:**

  - `POST /comments/` — Add a comment to a post
  - `GET /comments/?post={id}` — Get comments for a specific post
  - `PUT /comments/{id}/` — Update a comment
  - `DELETE /comments/{id}/` — Delete a comment

- **Likes:**
  - `POST /posts/{id}/like/` — Like a post
  - `DELETE /posts/{id}/like/` — Unlike a post

This diagram helps visualize how clients (like frontend apps) interact with the backend. It also ensures all necessary CRUD operations are covered and aligned with the API’s permissions and business logic.

---
