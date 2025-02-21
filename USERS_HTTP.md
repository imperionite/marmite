## Users

The subsequent images represent the screenshots captured from the sample HTTP calls related to `users or auth` to evaluate and validate the REST API endpoints. For this updates majority of the endpoints now are `protected` with access token provided by JWT except for the the **creation of new user** and **user login**. The compilation of sample HTTP requests generated from the [connectly-api](https://github.com/imperionite/marmite/tree/main/connectly-api) (Django REST API project) is available for review in the [rest.http file](https://github.com/imperionite/marmite/blob/main/rest.http).

### Create user - Public

POST /posts/users/

![create user](https://drive.google.com/uc?id=1VaKxgIw83Uk27qj2v2N5KMk2Z4cnIRTX)

### Fetch all users - Protected

GET /posts/users/

![all users](https://drive.google.com/uc?id=1MxkkouAmKWFfK4h_e7RNgqaQXkfAC8xz)

### Partial update by user id - Owner or Admin

PATCH /posts/users/{id}/

![partial update by id](https://drive.google.com/uc?id=19Ul9wKriWpsLRrhihmPmPJ3rizTc0W6d)

### Full update by user id - Owner or Admin

PUT /posts/users/{id}/

![full update by id](https://drive.google.com/uc?id=1ParXH1GYrESrXz4J-rfhgI83sBhfXwQk)

### Update user by user id with access token (JWT)

![unauthorized update](https://drive.google.com/uc?id=1ZAHjCTUz-6RwuGqYlzjYtXZik7bz8lE1)

### Delete user by id - Owner or Admin

DELETE /posts/users/{id}/

![delete user by id](https://drive.google.com/uc?id=1ELRnP2tOa9bqWwyQ8bhNoiupCv7RqdQi)

### Login by email - Public

POST /posts/users/login/ 

![login with email](https://drive.google.com/uc?id=1U8Yh4GU8V37_XNhZWzg5KJoNwIHq46_X)

### Login by username - Public

POST /posts/users/login/ 

![login with username](https://drive.google.com/uc?id=1GX_Qs-J0hZKfW0tYvwjaUtRwnrCsjo-3)