## Posts

The subsequent images represent the screenshots captured from the sample HTTP calls related to `posts` to evaluate and validate the REST API endpoints. For this updates majority of the endpoints now are `protected` with access token provided by JWT except for the the **creation of new user** and **user login**. The compilation of sample HTTP requests generated from the [connectly-api](https://github.com/imperionite/marmite/tree/main/connectly-api) (Django REST API project) is available for review in the [rest.http file](https://github.com/imperionite/marmite/blob/main/rest.http).

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
