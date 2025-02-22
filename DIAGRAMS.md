## Diagrams

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

**Why this matters:**  
This diagram helps visualize how clients (like frontend apps) interact with the backend. It also ensures all necessary CRUD operations are covered and aligned with the API’s permissions and business logic.

---
