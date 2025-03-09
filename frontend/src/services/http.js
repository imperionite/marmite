import axios from "axios";
import { jwtDecode } from "jwt-decode";
import qs from "qs";

const baseURL = "http://127.0.0.1:8000";

const http = axios.create({
  baseURL: baseURL,
  withCredentials: true,
  timeout: 90000,
});

// Function to get access token
const getAccessToken = () => {
  const jwtAtom = localStorage.getItem("jwtAtom");
  let token = jwtAtom ? JSON.parse(jwtAtom) : null;
  return token ? token.access : null;
};

// Function to get refresh token
const getRefreshToken = () => {
  const jwtAtom = localStorage.getItem("jwtAtom");
  let token = jwtAtom ? JSON.parse(jwtAtom) : null;
  return token ? token.refresh : null;
};

// Interceptor for requests
http.interceptors.request.use(
  (config) => {
    const token = getAccessToken();

    if (token) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }

    // Handle different Content-Types based on data
    if (config.data) {
      if (
        typeof config.data === "object" &&
        !(config.data instanceof FormData)
      ) {
        // For JSON data (excluding FormData), use the default "application/json"
        config.headers["Content-Type"] = "application/json";
      } else if (typeof config.data === "string") {
        // If data is already a string, assume it's URL-encoded
        config.headers["Content-Type"] = "application/x-www-form-urlencoded";
      } else if (config.data instanceof FormData) {
        // If data is FormData, let Axios handle the Content-Type
        delete config.headers["Content-Type"]; // Remove the default Content-Type
      }
    }

    //For x-www-form-urlencoded, transform the data
    if (
      config.headers["Content-Type"] === "application/x-www-form-urlencoded"
    ) {
      config.data = qs.stringify(config.data);
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor for responses
http.interceptors.response.use(
  (res) => res,
  async (err) => {
    const originalRequest = err.config;

    if (err.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = getRefreshToken();
        if (!refreshToken) {
          // No refresh token available, likely user is not logged in.
          console.error("No refresh token available.");
          // Example: window.location.href = '/login';
          return Promise.reject(err); // or a custom error
        }

        const tokenResponse = await axios.post(
          `${baseURL}/auth/jwt/refresh/`,
          { refresh: refreshToken },
          {
            withCredentials: true,
            timeout: 90000,
            headers: { "Content-Type": "application/json" },
          }
        );

        const { access: newAccessToken } = tokenResponse.data;

        // Retrieve the current tokens from localStorage
        let jwtTokenData = JSON.parse(localStorage.getItem("jwtAtom"));

        // Check if jwtAtom exists and contains both access and refresh tokens
        if (jwtTokenData && jwtTokenData.refresh) {
          // Only update the access token while retaining the refresh token
          jwtTokenData.access = newAccessToken;

          // Update the localStorage with the updated JWT object
          localStorage.setItem("jwtAtom", JSON.stringify(jwtTokenData));
        }
        // Decode the new access token and update expiration
        const decoded = jwtDecode(newAccessToken);
        localStorage.setItem("expAtom", JSON.stringify(decoded.exp * 1000)); // Store in milliseconds

        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`; // Use the new access token
        return http(originalRequest); // Retry the original request
      } catch (refreshError) {
        // Handle refresh token failure (e.g., refresh token expired)
        console.error("Failed to refresh token:", refreshError);
        // Redirect to login or clear tokens
        localStorage.removeItem("jwtAtom");
        localStorage.removeItem("expAtom");
        // Example: window.location.href = '/login';
        return Promise.reject(refreshError); // Or a custom error
      }
    }

    return Promise.reject(err);
  }
);

// API functions
const login = async (credentials) => {
  const response = await http.post("/posts/users/login/", credentials);
  return response.data;
};

const signup = async (userData) => {
  try {
    const response = await http.post("/posts/users/", userData);
    return response.data;
  } catch (error) {
    console.error("Signup error:", error);
    throw error;
  }
};

const fetchUser = async (userId) => {
  const response = await http.get("/posts/users/");
  return response.data.results.find((user) => user.id === userId); // paginated
};

const fetchPosts = async (userId) => {
  const response = await http.get("/posts/posts/");
  return response.data.results.filter((post) => post.author === userId); // paginated
};

const googleLogin = async (credential) => {
  const response = await http.post("/api/auth/social/google/", {
    access_token: credential,
  });
  return response.data;
};

export {
  login,
  signup,
  getAccessToken,
  getRefreshToken,
  fetchUser,
  fetchPosts,
  googleLogin,
};
