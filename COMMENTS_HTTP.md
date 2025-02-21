## Comments

The subsequent images represent the screenshots captured from the sample HTTP calls related to `comments` to evaluate and validate the REST API endpoints. For this updates majority of the endpoints now are `protected` with access token provided by JWT except for the the **creation of new user** and **user login**. The compilation of sample HTTP requests generated from the [connectly-api](https://github.com/imperionite/marmite/tree/main/connectly-api) (Django REST API project) is available for review in the [comments.http file](https://github.com/imperionite/marmite/blob/main/comments.http).


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
