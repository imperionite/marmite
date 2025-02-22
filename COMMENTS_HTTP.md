## Comments

The subsequent images represent the screenshots captured from the sample HTTP calls related to `comments` to evaluate and validate the REST API endpoints. For this updates majority of the endpoints now are `protected` with access token provided by JWT except for the the **creation of new user** and **user login**. The compilation of sample HTTP requests generated from the [connectly-api](https://github.com/imperionite/marmite/tree/main/connectly-api) (Django REST API project) is available for review in the [comments.http file](https://github.com/imperionite/marmite/blob/main/comments.http).


### User commenting on a specific post - Protected

POST /posts/posts/{id}/add_comment/

![commenting on a specific post](https://drive.google.com/uc?id=1a8VCTRBFdS-QJDhO_mbwiB2zf7juTrTi)

### Create comment - Protected

POST /posts/comments/

![create comment](https://drive.google.com/uc?id=17g99SuH0lLpjm7UPowxxNKcx7r_XQUuO)

### Fetch all comments - Public

GET /posts/comments/

![all comments](https://drive.google.com/uc?id=1AQbFmmkZX8SRCC9_q7ptSy7kFTR3i1EO)

### Update comment by id - Owner or Admin

PATCH /posts/comments/{id}/ or PUT /posts/comments/{id}/

![update comment by id](https://drive.google.com/uc?id=1qJbbG10NvOsdOn-C04cBMi9aEF6Se1MH)

### Delete comment by id - Owner or Admin

DELETE /posts/comments/{id}/

![delete comment by id](https://drive.google.com/uc?id=1tOseVV1ZIhMeAelnqB-q_mC2L-G6XRLZ)
