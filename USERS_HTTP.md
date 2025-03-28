## Users

The subsequent images represent the screenshots captured from the sample HTTP calls related to `users or auth` to evaluate and validate the REST API endpoints. For this updates majority of the endpoints now are `protected` with access token provided by JWT except for the the **creation of new user** and **user login**. The compilation of sample HTTP requests generated from the [connectly-api](https://github.com/imperionite/marmite/tree/main/connectly-api) (Django REST API project) is available for review in the [users.http file](https://github.com/imperionite/marmite/blob/main/users.http).

**Important Note Regarding Screenshot Data and Data Fixtures:**

Please be aware that some screenshots in this file were captured during the initial phases of development, _prior_ to the implementation of [Django data fixtures](https://docs.djangoproject.com/en/5.1/topics/db/fixtures/) for database seeding. As a result, the specific data values displayed in those earlier screenshots may not precisely match the data currently generated by the fixtures. However, the core API functionality and the expected behavior of the `/posts/users` endpoint, such as proper handling of requests and responses, remain consistent. New tests will explicitly utilize data generated by the fixtures to ensure ongoing alignment with the current database state. The purpose of including these screenshots is to demonstrate the initial API validation process. You may check the [README.md's Initial Data Seeding](https://github.com/imperionite/marmite/blob/main/README.md#ids) section for details.

**Initial Records in _user_ Table**

![user table](https://drive.google.com/uc?id=1I45Bhfrlg9x5BXvDUskIKj3oHtLaLJln)

---

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

### Validating JWT access token - Public but requires login to obtain the access token

POST /api/validate-token/

![validating JWT](https://drive.google.com/uc?id=1Rbw3mXYSwFGpY-FeXX6mCwnIU74ItHPn)

**Invalid Token**

![invalid JWT](https://drive.google.com/uc?id=1sKjwU70fXE90DhXl5wEekg0JUQHdxdRf)

### Obtaining New JWT Access Token From Refresh Token

POST /auth/jwt/refresh/

![new JWT](https://drive.google.com/uc?id=1RTQ6LZCT6OTC-ceq9NH07lyIlBlsPbsQ)

---

## Summary

### User API & Related Endpoints

#### Endpoints Table

| Endpoint               | Method | Description                                    | Image Link                                                                               |
| :--------------------- | :----- | :--------------------------------------------- | :--------------------------------------------------------------------------------------- |
| `/posts/users/`        | POST   | Create a new user                              | [Create User](https://drive.google.com/uc?id=1VaKxgIw83Uk27qj2v2N5KMk2Z4cnIRTX)          |
| `/posts/users/`        | GET    | Fetch all users                                | [All Users](https://drive.google.com/uc?id=1MxkkouAmKWFfK4h_e7RNgqaQXkfAC8xz)            |
| `/posts/users/{id}/`   | PATCH  | Partially update a user by ID (Owner or Admin) | [Partial Update by ID](https://drive.google.com/uc?id=19Ul9wKriWpsLRrhihmPmPJ3rizTc0W6d) |
| `/posts/users/{id}/`   | PUT    | Fully update a user by ID (Owner or Admin)     | [Full Update by ID](https://drive.google.com/uc?id=1ParXH1GYrESrXz4J-rfhgI83sBhfXwQk)    |
| `/posts/users/{id}/`   | DELETE | Delete a user by ID (Owner or Admin)           | [Delete User by ID](https://drive.google.com/uc?id=1ELRnP2tOa9bqWwyQ8bhNoiupCv7RqdQi)    |
| `/posts/users/login/`  | POST   | Login with email                               | [Login with Email](https://drive.google.com/uc?id=1U8Yh4GU8V37_XNhZWzg5KJoNwIHq46_X)     |
| `/posts/users/login/`  | POST   | Login with username                            | [Login with Username](https://drive.google.com/uc?id=1GX_Qs-J0hZKfW0tYvwjaUtRwnrCsjo-3)  |
| `/api/validate-token/` | POST   | Validate JWT access token                      | [Validating JWT](https://drive.google.com/uc?id=1Rbw3mXYSwFGpY-FeXX6mCwnIU74ItHPn)       |

##### Additional Verification and Error Cases

| Scenario            | Description                                                                              | Image Link                                                                              |
| :------------------ | :--------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------- |
| Unauthorized Update | Attempting to update a user without proper authorization (e.g., not the owner or admin). | [Unauthorized Update](https://drive.google.com/uc?id=1ZAHjCTUz-6RwuGqYlzjYtXZik7bz8lE1) |
| Invalid Token       | Using an invalid or expired JWT token.                                                   | [Invalid JWT](https://drive.google.com/uc?id=1sKjwU70fXE90DhXl5wEekg0JUQHdxdRf)         |
