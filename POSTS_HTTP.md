## Posts

The subsequent images represent the screenshots captured from the sample HTTP calls related to `posts` to evaluate and validate the REST API endpoints. For this updates majority of the endpoints now are `protected` with access token provided by JWT except for the the **creation of new user** and **user login**. The compilation of sample HTTP requests generated from the [connectly-api](https://github.com/imperionite/marmite/tree/main/connectly-api) (Django REST API project) is available for review in the [posts.http file](https://github.com/imperionite/marmite/blob/main/posts.http).

### Create post - Protected

POST /posts/posts/

![create post](https://drive.google.com/uc?id=1tx-eDLDo6L80G0pe5kNgBvWyZI77oYbf)

### Fetch all posts - Public

GET /posts/posts/

![all posts](https://drive.google.com/uc?id=1Tcnpl-TDkrRaHPLy7yc-GQrCoalZKLak)

### Partial update post by id - Owner/author

PATCH /posts/posts/{id}/

![update post by id](https://drive.google.com/uc?id=1C9XPQFKoVLUrgkY6n5wuX38fy2W_wvLL)

### Delete post by id - Owner/author

DELETE /posts/posts/{id}/

![delete post by id](https://drive.google.com/uc?id=1G2iEGpsgZe9hJlvYMmQO6SQcRtAuitDV)
