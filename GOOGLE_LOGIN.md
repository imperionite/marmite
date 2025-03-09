## Google Login

This assignment implements Google social login using Django Allauth, dj-rest-auth for the backend, and the `@react-oauth/google` library in the React frontend. Here’s an overview of the process and the approach taken to integrate this feature.

This implementation provides a solid foundation for Google social login, integrating Django Allauth and dj-rest-auth on the backend and leveraging `@react-oauth/google` in the React frontend. It ensures clear communication between the client and server, making the exchange of tokens and user authentication seamless and effective.

### Backend Setup (Django)

1. **Libraries Used:**
   - `django-allauth`: Handles social account registration and authentication.
   - `dj-rest-auth`: Provides REST API endpoints for user authentication and social login.

2. **Configuring Google in Django Admin:**
   - Add a new **SocialApp** entry for Google in the Django admin panel.
   - Use the **client ID** and **client secret** from your Google Console Developer project.
   - Ensure the site associated with this SocialApp matches your domain (like `localhost:8000` for development).

3. **Callback URL:**
   - Google requires a callback URL to redirect after a successful login. Set this in your Google Console:
     ```
     http://127.0.0.1:8000/accounts/google/login/callback/
     ```
   - This URL matches Django Allauth’s default endpoint for handling Google login responses.

#### URI's for Setup

<img src="https://drive.google.com/uc?id=1g8AfzwJTL9Fp7ERxRyn5TOSH6AbpVQtw" width="300" height="300" />


4. **API Endpoint:**
   - The frontend makes a POST request to `http://127.0.0.1:8000/api/auth/social/google/` and not the POST `/auth/google/login` as what is instructed in CAMU to exchange Google’s response for access and refresh tokens.

#### Frontend Homepage

![frontend homepage](https://drive.google.com/uc?id=1qq7p9l_wWNEe6A02I0exZLj7BVD1gg18)

## Frontend Setup (React)

1. **Libraries Used:**
   - `@react-oauth/google`: Provides the `useGoogleLogin` hook to handle Google login flow.
   - `tanstack/react-query`: Manages API call states and cache.
   - `jotai`: Manages global state for authentication tokens.

2. **Using the Google Login Hook:**
   The `useGoogleLogin` hook simplifies Google’s OAuth flow, generating the user’s credential (ID token) on success.

3. **Exchanging Tokens:**
   Once the Google login succeeds, the frontend sends the credential to the Django backend endpoint (`/api/auth/social/google/`) to exchange it for JWT access and refresh tokens.

4. **Challenges and Workaround:**
   - Due to difficulties testing this flow with REST clients alone, a dedicated frontend was built for more clarity on the implementation and API calls.
   - Security features were disabled during development for this assignment, as the current server setup can't supports HTTPS for this login approach.

### Frontend Login Page

![login page](https://drive.google.com/uc?id=1vnDcNIP5N7ozKp1dG8OAPt4aUGWb4CnL)

Endpoints that can be tested:

* POST /posts/users/ - normal login with username or email and password
* POST /api/auth/social/google/ - Google social login/user registration

### Google Signing in 

**Email Input**

![email login](https://drive.google.com/uc?id=1xaoKoRmfUgPdNo78lc86o16e5lT70dtt)

**Password Input**

![password login](https://drive.google.com/uc?id=1xaoKoRmfUgPdNo78lc86o16e5lT70dtt)

### Successful Login Redirect

![login redirect](https://drive.google.com/uc?id=1DCOFch8n0ZfdUGv8nIZz1OT-f_W3gQyg)

### New User Added Verification Via Google Social Login

**Admin Panel**

![via admin panel](https://drive.google.com/uc?id=1khwk7FKVcZn3tnNPS_9bJV-1sBwXHCW_)

**DB Query**

![via DB query](https://drive.google.com/uc?id=1_F11qOwbq7kdMPrnHQ4um0DFYSdFkYVA)

**API Call**

![via API calls](https://drive.google.com/uc?id=1lACjOzOe-VLPV22EYfzbmwIH8P_CtpgR)

