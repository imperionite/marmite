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

### Fetch post by id - Public

GET /posts/posts/{id}/

![post by id](https://drive.google.com/uc?id=1eyGABDfDBA9H5rEq4ukmq_g1casVAKVJ)

### Like post by id - Protected

POST /posts/posts/{id}/like/

![like post by id](https://drive.google.com/uc?id=1GZylyu8SGXTJo3en3ClKoHrUWAn0GMtp)


### Unlike a post by id - Protected

POST /posts/posts/{id}/unlike/

![unlike post by id](https://drive.google.com/uc?id=1mBpuyOFXwXwxj9kCWrI7Uxc2H6L-5Nb4)

### Like a post twice

![like post twice](https://drive.google.com/uc?id=1Q0IaxV6-I8gOXK9wiItK9n33h0yD_Ze9)

### Cannot unlike never liked post

![cannot unlike post](https://drive.google.com/uc?id=1dyDMnyECcuKY1083oGWiYPh3yuC-wh7m)

### User commenting on a specific post - Protected

POST /posts/posts/{id}/add_comment/

![commenting on a specific post](https://drive.google.com/uc?id=1a8VCTRBFdS-QJDhO_mbwiB2zf7juTrTi)
