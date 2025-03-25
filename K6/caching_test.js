import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '15s', target: 10 },
    { duration: '30s', target: 10 },
  ],
};

const BASE_URL = 'http://127.0.0.1:8000/posts';
let ACCESS_TOKEN = ''; // Initialize access token
const USER_ID = 13;
const POST_ID = 11;

// Function to obtain JWT token
function getAuthToken(username, password) {
  const payload = JSON.stringify({ identifier: username, password: password });
  const res = http.post(`${BASE_URL}/users/login/`, payload, {
    headers: { 'Content-Type': 'application/json' },
  });
  check(res, { 'Obtain JWT Token Status is 200': (r) => r.status === 200 });
  if (res.status === 200) {
    return res.json().access;
  }
  return null;
}

export default function () {
  // Obtain JWT token for user1
  if (!ACCESS_TOKEN) {
    ACCESS_TOKEN = `Bearer ${getAuthToken('user0', 'passworD1#')}`;
    if (!ACCESS_TOKEN) {
      console.error('Failed to obtain JWT token. Aborting test.');
      return;
    }
    console.log(`Obtained Access Token: ${ACCESS_TOKEN}`);
  }

  // Test feed caching
  let res = http.get(`${BASE_URL}/posts/feed/`, { headers: { Authorization: ACCESS_TOKEN } });
  check(res, { 'feed cache hit': (r) => r.status === 200 });

  // Test user profile caching
  res = http.get(`${BASE_URL}/users/${USER_ID}/`, { headers: { Authorization: ACCESS_TOKEN } });
  check(res, { 'user cache hit': (r) => r.status === 200 });

  // Test post caching
  res = http.get(`${BASE_URL}/posts/${POST_ID}/`, { headers: { Authorization: ACCESS_TOKEN } });
  check(res, { 'post cache hit': (r) => r.status === 200 });

  // Test comments caching
  res = http.get(`${BASE_URL}/posts/${POST_ID}/comments/`, { headers: { Authorization: ACCESS_TOKEN } });
  check(res, { 'comments cache hit': (r) => r.status === 200 });

  sleep(1);
}