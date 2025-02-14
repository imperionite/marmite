# marmite

The subsequent images represent the screenshots captured from the sample HTTP request and response executed to evaluate the REST API endpoints. The compilation of sample HTTP requests generated from the [connectly-api](https://github.com/imperionite/marmite/tree/main/connectly-api) (Django REST API project) is available for review in the [rest.http file](https://github.com/imperionite/marmite/blob/main/rest.http).

## Create user

POST /posts/users/


![create user](https://drive.google.com/uc?id=1VaKxgIw83Uk27qj2v2N5KMk2Z4cnIRTX)


## Fetch all users


GET /posts/users/ 

![all users](https://drive.google.com/uc?id=1RbHCg7FE7hhfwSJ8v1hL5gTa-qpqmEpO)

## Update user by user id 
Implementation of [ModelViewSet](https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset) and [DefaultRouter](https://www.django-rest-framework.org/api-guide/routers/#defaultrouter)/[SimpleRouter](https://www.django-rest-framework.org/api-guide/routers/#simplerouter) seamlessly provides all the functionalities to perform all CRUD operations with abstraction.

PUT /posts/users/{id}


![update user by id](https://drive.google.com/uc?id=1-9EN4hXWFgyzI7ULAQczXBJnEF39sOpD)


## Delete user by id

DELETE /posts/users/{id}

![delete user by id](https://drive.google.com/uc?id=1U44YweWqw-tS-Z1mKzdJDZi6ipU_qGN4)

## Create post


POST /posts/posts/


![create post](https://drive.google.com/uc?id=1d7_xg0gKN0q6YG4oMzTBJ8OvvfsZDzJR)


## Fetch all posts


GET /posts/posts/ 


![all posts](https://drive.google.com/uc?id=1xU6DPFmbO2Sjm1aB_adYgEHavJeCFhTM)



## Create comment


POST /posts/comments/


![create comment](https://drive.google.com/uc?id=1RIUpadp9FpS8NaOLFXN7EQl68TYDugx2)


## Fetch all comments


GET /posts/comments/ 


![all comments](https://drive.google.com/uc?id=17uEsmEY1YiOGALYUDODRf8Q3g4ocJvYZ)




