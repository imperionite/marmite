**Comprehensive list of endpoints** currently in this homework (Homework # 5)

---

## **1. Authentication Endpoints**
These endpoints handle user login and token-based authentication.

| Method | Endpoint               | Description |
|--------|------------------------|-------------|
| `POST` | `/posts/users/login/`  | Logs in a user and returns an access token (JWT). |
| `GET`  | `/posts/protected/`    | A protected route that only authenticated users can access. |
| `GET`  | `/posts/admin/`        | A route only accessible by admin users. |

---

## **2. User Endpoints**
Manage user creation, retrieval, update, and deletion.

| Method     | Endpoint            | Description |
|------------|---------------------|-------------|
| `POST`     | `/posts/users/`      | Register a new user. |
| `GET`      | `/posts/users/`      | Get a list of all users (only for authenticated users). |
| `GET`      | `/posts/users/{id}/` | Retrieve a specific user. |
| `PATCH`    | `/posts/users/{id}/` | Partially update user details (e.g., email, name). |
| `PUT`      | `/posts/users/{id}/` | Fully update a user. |
| `DELETE`   | `/posts/users/{id}/` | Delete a user (only by themselves or an admin). |

---

## **3. Post Endpoints**
Manage posts, likes, and comments.

| Method     | Endpoint                   | Description |
|------------|---------------------------|-------------|
| `POST`     | `/posts/`                  | Create a new post (authenticated users only). |
| `GET`      | `/posts/`                  | List all posts (accessible to everyone). |
| `GET`      | `/posts/{id}/`             | Retrieve a specific post with like & comment count. |
| `PUT`      | `/posts/{id}/`             | Fully update a post (only by the author). |
| `PATCH`    | `/posts/{id}/`             | Partially update a post (only by the author). |
| `DELETE`   | `/posts/{id}/`             | Delete a post (only by the author). |

---

## **4. Post Actions**
Additional actions related to posts, including likes and comments.

| Method     | Endpoint                   | Description |
|------------|---------------------------|-------------|
| `POST`     | `/posts/{id}/like/`        | Like a post (authenticated users only). |
| `POST`     | `/posts/{id}/unlike/`      | Unlike a post (authenticated users only). |
| `GET`      | `/posts/{id}/comments/`    | Retrieve all comments for a post (paginated). |

---

## **5. Comment Endpoints**
Manage comments on posts.

| Method     | Endpoint                   | Description |
|------------|---------------------------|-------------|
| `POST`     | `/posts/comments/`        | Create a comment on a post (authenticated users only). |
| `GET`      | `/posts/comments/`        | List all comments (open to all). |
| `GET`      | `/posts/comments/{id}/`   | Retrieve a specific comment. |
| `PATCH`    | `/posts/comments/{id}/`   | Update a comment (only by the comment author). |
| `PUT`      | `/posts/comments/{id}/`   | Fully update a comment (only by the comment author). |
| `DELETE`   | `/posts/comments/{id}/`   | Delete a comment (only by the comment author). |

---

## **6. Schema & API Documentation**
These are for API documentation purposes.

| Method | Endpoint | Description |
|--------|---------------------------|-------------|
| `GET`  | `/api/schema/`             | Retrieve the OpenAPI schema. |
| `GET`  | `/api/schema/swagger-ui/`   | View API documentation in Swagger UI. |
| `GET`  | `/api/schema/redoc/`        | View API documentation in ReDoc. |

---

## **Manual Testing Checklist**
1. **Authentication**  
   - Register a user.  
   - Login to get a JWT token.  
   - Access protected endpoints using the token.  

2. **Users**  
   - Create, retrieve, update, and delete users.  
   - Check that only authorized users can modify or delete their accounts.  

3. **Posts**  
   - Create, retrieve, update, and delete posts.  
   - Ensure only the author can modify or delete their posts.  

4. **Likes & Unlikes**  
   - Test liking and unliking a post.  
   - Ensure duplicate likes are prevented.  

5. **Comments**  
   - Test creating, updating, retrieving, and deleting comments.  
   - Ensure only comment authors can edit/delete their comments.  

6. **Permissions & Errors**  
   - Verify unauthorized users cannot create posts/comments.  
   - Check error responses for invalid requests (e.g., unliking a post that wasn't liked).  

---

Explicitly and implicitly required endpoints based on current `posts/views.py` and `posts/urls.py` files. 
---

## **Explicit Endpoints Verification** ✅

| **Method** | **Endpoint**             | **Exists in Your Code?** | **Location in Code** |
|------------|-------------------------|------------------------|----------------------|
| `POST`     | `/posts/users/login/`   | ✅ Yes | `LoginView` in `views.py` |
| `POST`     | `/posts/`               | ✅ Yes | `create()` in `PostViewSet` |
| `GET`      | `/posts/{id}/`          | ✅ Yes | `retrieve()` in `PostViewSet` |
| `POST`     | `/posts/{id}/like/`     | ✅ Yes | `like()` action in `PostViewSet` |
| `POST`     | `/posts/{id}/unlike/`   | ✅ Yes | `unlike()` action in `PostViewSet` |
| `GET`      | `/posts/{id}/comments/` | ✅ Yes | `comments()` action in `PostViewSet` |

💡 **Conclusion**: Your project **already includes** all explicitly required endpoints. No extra implementation is needed!

---

## **Implicit Endpoints Verification** ✅

| **Method** | **Endpoint**            | **Exists in Your Code?** | **Location in Code** |
|------------|------------------------|------------------------|----------------------|
| `POST`     | `/posts/users/`        | ✅ Yes | `create()` in `UserViewSet` |
| `GET`      | `/posts/users/{id}/`   | ✅ Yes | `retrieve()` in `UserViewSet` |
| `PATCH`    | `/posts/users/{id}/`   | ✅ Yes | `update()` in `UserViewSet` |
| `DELETE`   | `/posts/users/{id}/`   | ✅ Yes | `destroy()` in `UserViewSet` |
| `GET`      | `/posts/`              | ✅ Yes | `list()` (default) in `PostViewSet` |
| `PUT/PATCH`| `/posts/{id}/`         | ✅ Yes | `update()` in `PostViewSet` |
| `DELETE`   | `/posts/{id}/`         | ✅ Yes | `destroy()` in `PostViewSet` |
| `POST`     | `/posts/comments/`     | ✅ Yes | `create()` in `CommentViewSet` |
| `GET`      | `/posts/comments/`     | ✅ Yes | `list()` (default) in `CommentViewSet` |
| `PUT/PATCH`| `/posts/comments/{id}/`| ✅ Yes | `update()` in `CommentViewSet` |
| `DELETE`   | `/posts/comments/{id}/`| ✅ Yes | `destroy()` in `CommentViewSet` |

---

