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
  const feedUrl = `${API_BASE_URL}/feed/?page=1`;

  group('Get Feed Test', () => {
    // Initial request
    const res1 = http.get(feedUrl, { headers });
    check(res1, {
      'Get Feed (Initial) - status is 200': (r) => r.status === 200,
      'Get Feed (Initial) - is JSON': (r) => r.headers['Content-Type'] && r.headers['Content-Type'].includes('application/json'),
      'Get Feed (Initial) - has data': (r) => {
        try {
          return JSON.parse(r.body).results && JSON.parse(r.body).results.length >= 0;
        } catch (e) {
          console.error('Error parsing initial feed response:', e);
          return false;
        }
      },
    });

    sleep(0.5);

    // Cached request
    const res2 = http.get(feedUrl, { headers });
    check(res2, {
      'Get Feed (Cached) - status is 200': (r) => r.status === 200,
      'Get Feed (Cached) - is JSON': (r) => r.headers['Content-Type'] && r.headers['Content-Type'].includes('application/json'),
      'Get Feed (Cached) - has data': (r) => {
        try {
          return JSON.parse(r.body).results && JSON.parse(r.body).results.length >= 0;
        } catch (e) {
          console.error('Error parsing cached feed response:', e);
          return false;
        }
      },
    });

    // Check response time for caching (expect faster second request)
    check(res2, {
      'Get Feed (Cached) - response is faster': () => res2.timings.duration < res1.timings.duration,
    });
  });

  sleep(1);
}
