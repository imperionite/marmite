#!/bin/bash

docker-compose run --rm K6 run /tests/caching_test.js
# docker-compose run --rm k6 run /tests/rate_limit_test.js
# docker-compose run --rm k6 run /tests/cache_invalidation_test.js