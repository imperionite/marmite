import http from 'k6/http';
import { check, sleep, group } from 'k6';

export const options = {
  stages: [
    { duration: '10s', target: 10 },
    { duration: '30s', target: 10 },
    { duration: '10s', target: 0 },
  ],
};

const API_BASE_URL = 'http://localhost:8000/posts';
const LOGIN_URL = `${API_BASE_URL}/users/login/`;
const TEST_USERNAME = 'user18';
const TEST_PASSWORD = 'passworD1#';
const POST_IDS_WITH_COMMENTS = [1, 2, 3]; // Example post IDs

let accessToken;

export function setup() {
  const loginPayload = JSON.stringify({
    identifier: TEST_USERNAME,
    password: TEST_PASSWORD,
  });

  const loginHeaders = { 'Content-Type': 'application/json' };
  const loginRes = http.post(LOGIN_URL, loginPayload, { headers: loginHeaders });

  check(loginRes, {
    'Login - status is 200': (r) => r.status === 200,
    'Login - contains token': (r) => r.json('access') !== undefined,
  });

  if (loginRes.status !== 200) {
    console.error('Login failed:', loginRes.body);
    throw new Error('Login failed');
  }

  return { accessToken: loginRes.json('access') };
}

export default function ({ accessToken }) {
  const headers = {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json',
  };
  const postId = POST_IDS_WITH_COMMENTS[Math.floor(Math.random() * POST_IDS_WITH_COMMENTS.length)];
  const commentsUrl = `${API_BASE_URL}/posts/${postId}/comments/?page=1`;

  group('Get Comments Test', () => {
    // Initial request
    const res1 = http.get(commentsUrl, { headers });
    check(res1, {
      'Get Comments (Initial) - status is 200': (r) => r.status === 200,
      'Get Comments (Initial) - is JSON': (r) => r.headers['Content-Type'] && r.headers['Content-Type'].includes('application/json'),
      'Get Comments (Initial) - has results': (r) => {
        try {
          return JSON.parse(r.body).results && JSON.parse(r.body).results.length >= 0;
        } catch (e) {
          console.error('Error parsing initial comments response:', e);
          return false;
        }
      },
      'Get Comments (Initial) - first comment has content': (r) => {
        try {
          const data = JSON.parse(r.body);
          return data.results && data.results.length > 0 && data.results[0].content !== undefined;
        } catch (e) {
          console.error('Error parsing initial comments response for content check:', e);
          return false;
        }
      },
    });

    sleep(0.5);

    // Cached request
    const res2 = http.get(commentsUrl, { headers });
    check(res2, {
      'Get Comments (Cached) - status is 200': (r) => r.status === 200,
      'Get Comments (Cached) - is JSON': (r) => r.headers['Content-Type'] && r.headers['Content-Type'].includes('application/json'),
      'Get Comments (Cached) - has results': (r) => {
        try {
          return JSON.parse(r.body).results && JSON.parse(r.body).results.length >= 0;
        } catch (e) {
          console.error('Error parsing cached comments response:', e);
          return false;
        }
      },
    });

    // Check response time for caching (expect faster second request)
    check(res2, {
      'Get Comments (Cached) - response is faster': () => res2.timings.duration < res1.timings.duration,
    });
  });

  sleep(1);
}