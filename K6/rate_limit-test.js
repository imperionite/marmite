import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 50, // 50 virtual users
  duration: '10s', // Run for 10 seconds
};

const BASE_URL = 'https://127.0.0.1:8080'; // test with nginx and https
const ACCESS_TOKEN = 'Bearer your_access_token'; // Replace with a valid access token
const POST_ID = 1; // Replace with a valid post ID

export default function () {
  // Test post creation rate limiting
  let payload = JSON.stringify({ content: 'Test post content', privacy: 'public' });
  let params = { headers: { 'Content-Type': 'application/json', Authorization: ACCESS_TOKEN } };
  let res = http.post(`${BASE_URL}/posts/`, payload, params);
  check(res, { 'post rate limit': (r) => r.status === 201 || r.status === 429 });

  // Test comment creation rate limiting
  payload = JSON.stringify({ content: 'Test comment content' });
  res = http.post(`${BASE_URL}/posts/${POST_ID}/comments/`, payload, params);
  check(res, { 'comment rate limit': (r) => r.status === 201 || r.status === 429 });

  // Test follow creation rate limiting
  payload = JSON.stringify({ following: 2 }); // Replace 2 with a valid user ID to follow
  res = http.post(`${BASE_URL}/follows/`, payload, params);
  check(res, { 'follow rate limit': (r) => r.status === 201 || r.status === 429 });
}