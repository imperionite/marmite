# Homework 8: Privacy Settings and Role-Based Access Control (RBAC)

**1. RBAC Tests:**

## **Test Case 1: Admin User Deletes a Post:**

* **Scenario:** Admin user (user0, ID: 2) deletes a post created by another user (user1, ID: 3).
* **Prerequisites:** Login as user0 (admin). Use the login endpoint and store the access token.
* **Endpoint:** `DELETE /posts/posts/3/`

### Initial posts
![initial posts in db](https://drive.google.com/uc?id=1c-Qo7okus2MW_Ye2M0ZTr03mn3vaMNqm)

#### Admin deletes a post
![admin user deletes a post](https://drive.google.com/uc?id=1XaMV7fv0-xRsh8J2nszNd31KGUkauUbY)

### Posts after deletion
![after admin user deletes a post](https://drive.google.com/uc?id=1CMos0vxzk551Oi5yzZwfPOymxwtYYW0L)

---
## * **Test Case 2: Admin User Deletes a Comment:**
* **Scenario:** Admin user (user0, ID: 2) deletes a comment created by another user (user1, ID: 1).
* **Prerequisites:** Login as user0 (admin).
* **Endpoint:** `DELETE /comments/1/`

### Initial comments

![initial comments in db](https://drive.google.com/uc?id=1EqU6NbqdAEKHotjJOilP5rg6bSFknJl3)

#### Admin deletes a comment

![admin user deletes a comment](https://drive.google.com/uc?id=1rkkBk080IGlzgBxD2fU7rI_BckF14ees)

### Comments after deletion

![after admin user deletes a comment](https://drive.google.com/uc?id=1PS9Vr_M-JZdcVr-YD5gLu-Giji6UtaAe)

--- 
## **Test Case 3: Admin User Updates a User:**
* **Scenario:** Admin user (user0, ID: 2) updates the username of user1 (ID: 3).
* **Prerequisites:** Login as user0 (admin).
* **Endpoint:** `PATCH /users/3/`

### Initial users

![initial users in db](https://drive.google.com/uc?id=1jZzO4sxpj7DWEdRYXfdasTZ69OuOkFYe)

#### Admin update a user

![admin user deletes a comment](https://drive.google.com/uc?id=1DZB_mTlXtAe6-zp4pbQ3B3GKjEi5_AUE)

### Users after update

![after admin user deletes a comment](https://drive.google.com/uc?id=1d78txIvUNDERYxLjJcpEQMWEfWaucFHS)

---
## * **Test Case 4: Regular User Deletes Own Post:**
* **Scenario:** Regular user (user1, ID: 3) deletes their own post (ID: 3).
* **Prerequisites:** Login as user1.
* **Endpoint:** `DELETE /posts/3/`

![regular user deletes own post](https://drive.google.com/uc?id=1PqyQQTJlxhhpQg5LvuWDBIGBm-MKsi92)

---
## * **Test Case 5: Regular User Deletes Another User's Post:**
* **Scenario:** Regular user (user1, ID: 3) attempts to delete a post created by user0 (ID: 2).
* **Prerequisites:** Login as user1.
* **Endpoint:** `DELETE /posts/1/`

![regular user deletes own post](https://drive.google.com/uc?id=1zH_5P4DAUJz6R2iXaZyZ2_RQnzBsznHm)

---
 
## **Test Case 6: Regular User Deletes Another User's Comment:**
* **Scenario:** Regular user (user1, ID: 3) attempts to delete a comment created by user0 (ID:2).
* **Prerequisites:** Login as user1.
* **Endpoint:** `DELETE /comments/3/`

![regular user deletes another user's comment](https://drive.google.com/uc?id=15oj4KazYDOzVBWuuNdaOQNuM2nqt0vbE)

---
## **Test Case 7: Guest User Accesses Protected Routes:**
* **Scenario:** Guest user attempts to access the feed.
* **Endpoint:** `GET /posts/feed/`

![guest user accesses protected endpoint](https://drive.google.com/uc?id=11d2CSGmIAltczvYAEBTSTRrv4Xi9GYXt)

---
**2. Privacy Settings Tests:**

## **Test Case 8: Public Post Visibility:**
    * **Scenario:** User2 (ID: 4) views public post 1.
    * **Prerequisites:** Login as user2.
    * **Endpoint:** `GET /posts/1/`

### All Public Posts

![all public posts](https://drive.google.com/uc?id=169himHJWZ7N5ETsAO3EYPlBGLp3PKv0I)

---
* **Test Case 9: Public Post in Feed:**
    * **Scenario:** User2 views public post 1 in the feed.
    * **Prerequisites:** Login as user2.
    * **Endpoint:** `GET /posts/feed/`
    * **Headers:** `Authorization: Bearer <access_token>`
    * **Expected Result:** Status code 200 (OK), and post 1 is included in the feed.
* **Test Case 10: Private Post Visibility (Owner):**
    * **Scenario:** User0 (ID: 2) views their own private post 6.
    * **Prerequisites:** Login as user0.
    * **Endpoint:** `GET /posts/6/`
    * **Headers:** `Authorization: Bearer <access_token>`
    * **Expected Result:** Status code 200 (OK), and the post content is visible.
* **Test Case 11: Private Post Visibility (Other User):**
    * **Scenario:** User1 (ID: 3) attempts to view user0's private post 6.
    * **Prerequisites:** Login as user1.
    * **Endpoint:** `GET /posts/6/`
    * **Headers:** `Authorization: Bearer <access_token>`
    * **Expected Result:** Status code 403 (Forbidden).
* **Test Case 12: Private Post in Feed (Other User):**
    * **Scenario:** User1 views the feed and private post 6 from user0 is not visible.
    * **Prerequisites:** Login as user1.
    * **Endpoint:** `GET /posts/feed/`
    * **Headers:** `Authorization: Bearer <access_token>`
    * **Expected Result:** Status code 200 (OK), and post 6 is not included in the feed.

Please let me know how these tests go, and if you have any questions or encounter any issues!
