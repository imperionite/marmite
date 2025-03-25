import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 5 }, // Ramp up to 5 virtual users over 30 seconds
    { duration: '60s', target: 5 }, // Maintain 5 virtual users for 60 seconds
  ],
};

const BASE_URL = 'https://127.0.0.1:8080'; // test with nginx and https
const ACCESS_TOKEN = 'Bearer your_access_token'; // Replace with a valid access token
const USER_ID = 2; // Replace with a valid user ID
const POST_ID = 1; // Replace with a valid post ID

export default function () {
  // Create a post to invalidate feed cache
  let payload = JSON.stringify({ content: 'Test post to invalidate cache', privacy: 'public' });
  let params = { headers: { 'Content-Type': 'application/json', Authorization: ACCESS_TOKEN } };
  http.post(`${BASE_URL}/posts/`, payload, params);
  sleep(1);

  // Check feed cache after invalidation
  let res = http.get(`${BASE_URL}/posts/feed/`, { headers: { Authorization: ACCESS_TOKEN } });
  check(res, { 'feed cache invalidated': (r) => r.status === 200 });

  // Update a user to invalidate user cache
  payload = JSON.stringify({ username: 'new_username' });
  res = http.patch(`${BASE_URL}/users/${USER_ID}/`, payload, params);
  check(res, { 'user cache invalidated': (r) => r.status === 200 });

  // Delete a follow relationship to invalidate follow cache
  res = http.del(`${BASE_URL}/follows/1/`, null, params); // Replace 1 with a valid follow ID
  check(res, { 'follow cache invalidated': (r) => r.status === 204 });

  sleep(1);
}