# Feeds

The subsequent images represent the screenshots captured from the sample HTTP calls related to `feeds` to evaluate and validate the REST API endpoints. 

## Unit Test

Test case in `posts/tests.py`.

![feeds test case](https://drive.google.com/uc?id=17HwP6pvgaq88A-M4j07uSZO2kQR5O2pA)

- The test suite for the `/feed/` endpoint validates its core functionalities:
  - Basic retrieval of the feed
  - Filtering based on user preferences
  - Authentication requirements
- The `setUp` method initializes the testing environment by:
  - Creating several user accounts
  - Creating a set of posts
  - Setting up a follow relationship between two users
  - Simulating a like action from one user to a post
- The test cases:
  - **test_feed_view_authenticated**: Verifies that an authenticated user can retrieve the feed successfully, ensuring a 200 OK response and the correct number of posts.
  - **test_feed_view_followed_filter**: Checks the filtering of posts from followed users, ensuring that only posts from users the authenticated user is following are included in the response.
  - **test_feed_view_liked_filter**: Validates the filtering for liked posts, ensuring that only posts liked by the authenticated user are returned.
  - **test_feed_view_unauthenticated**: Confirms that unauthenticated users are denied access to the feed, resulting in a 401 UNAUTHORIZED response.
- These tests ensure the `/feed/` endpoint’s reliability and adherence to its specifications.


### Basic Feed w/out query parameters

GET /posts/feed/

![basic feed](https://drive.google.com/uc?id=1isdDlDDeHhS2ORQP6YVRMx66eOWX2C2H)


### Followed Feed

GET /posts/feed/?filter=followed

![followed feed](https://drive.google.com/uc?id=1IPyhsKDhJ_CaWxxkPmjcRR65TFRVBWts)


### Liked Feed

GET /posts/feed/?filter=liked


![liked feed](https://drive.google.com/uc?id=1RLmCZTuoeyPkyF1tAgACj3scjn6aomJy)


### Creates New Follow Relationship

POST /posts/follows/

![create follow](https://drive.google.com/uc?id=1BZXwSFYKRLU7pY40fml9r1YzAs3J1ZlQ)

### Retrieves All Follows

GET /posts/follows/

![all follows relationships](https://drive.google.com/uc?id=1hl483pGPvrSGLAqc7vMqhbnSZy3mFAUG)


### Delete Follow Relationship by Owner

DELETE /posts/follows/{follow_id}/

![delete follow](https://drive.google.com/uc?id=1ECLekShOkkqcbyGrc7Oi1rczY3yyxI0q)

