# marmite

The subsequent images represent the screenshots captured from the sample HTTP request and response executed to evaluate the REST API endpoints. The compilation of sample HTTP requests generated from the [connectly-api](https://github.com/imperionite/marmite/tree/main/connectly-api) (Django REST API project) is available for review in the [rest.http file](https://github.com/imperionite/marmite/blob/main/rest.http).

**General notes on my implementation of all CRUD operations (CREATE, READ, UPDATE, DELETE):**

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

## For User

### Create user

POST /posts/users/

![create user](https://drive.google.com/uc?id=1VaKxgIw83Uk27qj2v2N5KMk2Z4cnIRTX)

### Fetch all users

GET /posts/users/

![all users](https://drive.google.com/uc?id=1RbHCg7FE7hhfwSJ8v1hL5gTa-qpqmEpO)

### Update user by user id

PATCH /posts/users/{id}/ or PUT /posts/users/{id}/

![update user by id](https://drive.google.com/uc?id=1-9EN4hXWFgyzI7ULAQczXBJnEF39sOpD)

### Delete user by id

DELETE /posts/users/{id}/

![delete user by id](https://drive.google.com/uc?id=1U44YweWqw-tS-Z1mKzdJDZi6ipU_qGN4)

## For Post

### Create post

POST /posts/posts/

![create post](https://drive.google.com/uc?id=1d7_xg0gKN0q6YG4oMzTBJ8OvvfsZDzJR)

### Fetch all posts

GET /posts/posts/

![all posts](https://drive.google.com/uc?id=1xU6DPFmbO2Sjm1aB_adYgEHavJeCFhTM)

### Update post by id

PATCH /posts/posts/{id}/ or PUT /posts/posts/{id}/

![update post by id](https://drive.google.com/uc?id=1Jk5xFnEY8iewLTDV7gSj8luCX3IkZV6S)

### Delete post by id

DELETE /posts/posts/{id}/

![delete post by id](https://drive.google.com/uc?id=1zu9rvaFjB0njyqfxXFH96gEILbtsI5ZF)

## For Comment

### Create comment

POST /posts/comments/

![create comment](https://drive.google.com/uc?id=1RIUpadp9FpS8NaOLFXN7EQl68TYDugx2)

### Fetch all comments

GET /posts/comments/

![all comments](https://drive.google.com/uc?id=17uEsmEY1YiOGALYUDODRf8Q3g4ocJvYZ)

### Update comment by id

PATCH /posts/comments/{id}/ or PUT /posts/comments/{id}/

![update comment by id](https://drive.google.com/uc?id=1o4QtF4i4VRmZZ7IHS7aGhhwaMFISXrYf)

### Delete comment by id

DELETE /posts/comments/{id}/


![delete comment by id](https://drive.google.com/uc?id=1lGfCwxRFFc4ZwgmSesbKM_t9ZW7Spsou)