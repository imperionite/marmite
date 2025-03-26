## **Caching Documentation and Validation**

### **Assessment and Interpretation of k6 Performance Test Results for the Connectly Posts Feed Endpoint**

This report provides an assessment and interpretation of the performance test results obtained using k6 for the Connectly application's feed endpoint. The primary objective of the test was to evaluate the endpoint's reliability and performance, particularly focusing on the effectiveness of caching mechanisms under a simulated load.

![Feed Test](https://drive.google.com/uc?id=1L7E5r3KNRDS_rZYkMmgbs1J6O6WZzqgj)

**Methodology:**

The performance test was conducted using a k6 script ([K6/feed-test.js](https://github.com/imperionite/marmite/blob/main/K6/feed-test.js)) executed locally. The script simulated a user logging in and then repeatedly fetching the feed. The test configuration involved a ramping virtual user (VU) scenario over a duration of 50 seconds, reaching a peak of 10 concurrent VUs. The test consisted of three stages:

1.  **Ramp-up (10s):** The number of VUs gradually increased from 0 to 5.
2.  **Steady State (20s):** The test maintained a constant load of 10 VUs.
3.  **Ramp-down (10s):** The number of VUs gradually decreased from 10 to 0.

The script included checks to verify:

- Successful login (status code 200, presence of a token).
- Successful retrieval of the feed for both initial (uncached) and subsequent (cached) requests (status code 200, JSON format, presence of data).
- Whether the response time for cached requests was faster than the initial requests.

**Interpretation of Results:**

The k6 test results indicate a generally healthy performance profile for the Connectly feed endpoint under the tested load. However, there is a notable observation regarding the effectiveness of the caching mechanism.

- **Successful Request Handling:** The absence of any HTTP request failures (`http_req_failed: 0.00%`) signifies that the endpoint successfully handled all requests throughout the test duration. This suggests a stable and reliable API, capable of serving requests without encountering server-side errors under the tested load.
- **High Check Success Rate:** The overall check success rate of 93.36% demonstrates that the majority of assertions regarding the API's behavior were met. This includes successful login and retrieval of feed data in the expected format for both initial and cached requests.
- **Acceptable Response Times:** The average HTTP request duration of 8.45ms, with the 95th percentile at 9.96ms, suggests that the endpoint provides a responsive user experience. These metrics indicate that the application is serving feed data relatively quickly, even under a concurrent user load of 10.
- **Caching Inefficiency:** The primary area of concern lies in the failing check: `Get Feed (Cached) - response is faster`, which had a success rate of only 53%. This implies that for nearly half of the requests intended to be served from the cache, the response time was not measurably faster than the initial, presumably uncached, requests.

**Potential Implications of Caching Inefficiency:**

The failure of the cached response time check suggests that the caching mechanism, while functional (as evidenced by successful data retrieval), might not be providing the expected performance benefits. Several factors could contribute to this:

- **Overhead of Caching:** The process of retrieving data from the cache (e.g., accessing Redis, deserialization) might introduce overhead that negates the performance gains from avoiding database queries, especially if the uncached response is already very fast.
- **Suboptimal Cache Hit Rate:** While the test design aimed to hit the cache on subsequent requests, the cache hit rate might be lower than expected due to factors such as cache invalidation policies or slight variations in request parameters.
- **Network Latency:** Minor variations in network latency could obscure the performance difference between cached and uncached responses, particularly if the backend processing time is already very low.
- **Resource Contention:** The caching server (e.g., Redis) might be experiencing resource contention, leading to slower retrieval times.

**Recommendations:**

1.  **Further Investigation of Caching Performance:** A more detailed analysis of the response times for initial and cached requests is warranted. Examining the raw data or using more granular metrics (e.g., p50, p99) might reveal subtle differences not captured by a simple "faster" check.
2.  **Profiling Backend Operations:** Profiling the Django backend during the test could help identify specific bottlenecks in both cached and uncached scenarios. This could reveal the overhead associated with cache retrieval.
3.  **Review Caching Configuration:** Re-evaluating the cache timeout, invalidation strategies, and the efficiency of the cache serialization/deserialization process might lead to performance improvements.
4.  **Monitoring Redis Performance:** If Redis is used for caching, monitoring its performance metrics (latency, CPU usage, memory usage) is crucial to identify potential bottlenecks.
5.  **Refine k6 Check:** The "response is faster" check might need adjustment. Instead of a simple boolean comparison, consider checking if the cached response time is significantly faster (e.g., by a certain percentage or absolute time difference).

**Conclusion:**

The k6 test results indicate that the Connectly feed endpoint is performing reliably under the tested load. However, the caching mechanism does not consistently demonstrate a performance advantage. Further investigation is needed to understand the reasons behind this inefficiency and to optimize the caching strategy for improved performance. Addressing this could lead to a more responsive application, especially under higher load scenarios.

---

### **Assessment and Interpretation of k6 Performance Test Results for the Connectly Comments Endpoint**

This report provides an assessment and interpretation of the performance test results obtained using k6 for the Connectly application's comments endpoint. The primary objective was to evaluate the endpoint's reliability and performance, with a focus on data integrity and caching effectiveness under a simulated load.

![Comment Test](https://drive.google.com/uc?id=11jfKicfYhK9970GDbpwJhLhOAVLwIj4X)

**Methodology:**

The performance test was conducted using a k6 script ([K6/comment-test.js](https://github.com/imperionite/marmite/blob/main/K6/comment-test.js)) executed locally. The script simulated a user logging in and then repeatedly fetching comments for a randomly selected post. Similar to the feed test, the test employed a ramping virtual user (VU) scenario over a duration of 50 seconds, reaching a peak of 10 concurrent VUs. The test consisted of three stages:

1.  **Ramp-up (10s):** The number of VUs gradually increased from 0 to 10.
2.  **Steady State (30s):** The test maintained a constant load of 10 VUs.
3.  **Ramp-down (10s):** The number of VUs gradually decreased from 10 to 0.

The script included checks to verify:

- Successful login (status code 200, presence of a token).
- Successful retrieval of comments for both initial (uncached) and subsequent (cached) requests (status code 200, JSON format, presence of results).
- The presence of content in the first comment of the initial request.
- Whether the response time for cached requests was faster than the initial requests.

**Interpretation of Results:**

The k6 test results indicate a generally stable performance for the Connectly comments endpoint under the tested load. However, there are key issues identified regarding data integrity and caching efficiency that require attention.

- **Successful Request Handling:** The absence of HTTP request failures (`http_req_failed: 0.00%`) indicates that the endpoint successfully processed all requests without encountering server-side errors during the test. This suggests a reliable API in terms of basic request handling.
- **Good Overall Check Success Rate:** The overall check success rate of 89.13% suggests that most of the assertions about the API's behavior were met. This includes successful login and retrieval of comments data in the expected format for both initial and cached requests.
- **Acceptable Response Times:** The average HTTP request duration of 12.79ms, with the 95th percentile at 14.21ms, indicates that the endpoint provides a reasonably responsive experience. These latencies are slightly higher than the feed endpoint but still generally acceptable for API interactions.
- **Data Integrity Issue:** A significant failure is observed in the check `Get Comments (Initial) - first comment has content`, which had a success rate of only 63%. This indicates that for a substantial portion of the initial requests, the first comment in the response did not contain the expected content. This points to a potential issue with data retrieval or serialization, where comments are being returned without their content.
- **Caching Inefficiency:** Similar to the feed endpoint, the check `Get Comments (Cached) - response is faster` shows a low success rate of 49%. This suggests that the caching mechanism is not consistently providing the anticipated performance benefits for subsequent requests. In almost half of the cases, the cached response was not faster than the initial one.

**Potential Implications:**

- **Data Integrity:** The failure of the content check is a critical issue. Users expect comments to have content, and this failure suggests a bug in the comment retrieval or serialization process, potentially leading to a poor user experience.
- **Caching Inefficiency:** The inconsistent performance improvement from caching indicates that the caching mechanism might be poorly configured, experiencing overhead that negates its benefits, or not being hit as frequently as expected. This can lead to unnecessary load on the database and slower response times than anticipated.

**Recommendations:**

* **Investigate Data Integrity Issue:** The primary focus should be on diagnosing and resolving the reason why the content of the first comment is missing in a significant number of initial requests. This requires examining the Django view logic, serializer, and database queries involved in fetching comments. Logging the specific data being retrieved and serialized during these failing requests could be invaluable.
* **Analyze Caching Performance:** Conduct a deeper analysis of the response times for both initial and cached requests. Examine percentiles and consider implementing logging on the Django side to explicitly track cache hits and misses for the comments endpoint.
* **Review Caching Configuration for Comments:** Evaluate the cache timeout and invalidation strategy for the comments endpoint. Ensure it aligns with the expected data update frequency and performance goals.
* **Profile Backend Operations:** Profiling the Django backend specifically for the comments endpoint can help identify performance bottlenecks in both cached and uncached scenarios.
* **Examine Database Queries:** Analyze the database queries executed when fetching comments. Ensure they are optimized and that appropriate indexes are in place.

**Conclusion:**

The k6 test reveals a significant data integrity issue in the comments endpoint, where comment content is frequently missing. Additionally, the caching mechanism is not consistently providing performance benefits. Addressing the data integrity problem is paramount, as it directly impacts the functionality of the application. Simultaneously, investigating and optimizing the caching strategy is crucial for improving the responsiveness and scalability of the comments feature. Further investigation using Django logs, profiling tools, and more granular k6 metrics is strongly recommended.

---

### **Report on Cache Hit Rate Analysis for Post Feed Test**

The purpose of this report is to analyze the Redis cache performance before and after running the feed-test script. This is done by computing the cache hit rate, which indicates how effectively the cache serves requests without requiring a database query. The cache hit rate is calculated using the formula:

$$
\text{Cache Hit Rate} = \frac{\text{Keyspace Hits}}{\text{Keyspace Hits} + \text{Keyspace Misses}} \times 100
$$

**Data Source:** `INFO stats` command from Redis before and after running the `feed-test` script.

**Metrics Used:**

- `keyspace_hits`: Number of successful lookups in the key space.
- `keyspace_misses`: Number of unsuccessful lookups in the key space.

**Info Stats before running the feed test script**

![Info Stats Before Running the Feed Test Script](https://drive.google.com/uc?id=1KDQ8MKw4Av4pSdzR-fVKkh6iTEOa8yNQ)

**Info Stats after running the feed test script**

![Info Stats After Running the Feed Test Script](https://drive.google.com/uc?id=1jM21Wr9nSWkhpBk6QASB04d7JRW2vgGW)

**Cache Statistics Overview**

| Metric                     | Before Test | After Test | Difference |
| -------------------------- | ----------- | ---------- | ---------- |
| Total Connections Received | 26          | 28         | +2         |
| Total Commands Processed   | 3627        | 4176       | +549       |
| Keyspace Hits              | 3480        | 4022       | +542       |
| Keyspace Misses            | 1           | 1          | 0          |
| Cache Hit Rate (%)         | 99.97       | 99.98      | +0.01      |

**Interpretation**

- **High Cache Efficiency**: The cache hit rate before the test was 99.97% and increased slightly to 99.98% after the test. This demonstrates that almost all requests were successfully served from the cache, minimizing database queries and reducing system load.
- **Minimal Cache Misses**: The number of keyspace misses remained constant at 1 before and after the test, meaning there was no significant increase in cache misses even with additional requests.
- **Stable Performance**: The total number of keyspace hits increased by 542, which aligns with the number of additional commands processed (+549). This suggests that the caching mechanism is working efficiently and serving the expected volume of requests.
- **Low Eviction and Expiry Rates**: There were no evicted keys or expired keys recorded, indicating that the cache has sufficient memory and is not under strain.

While the global cache hit rate is impressively high, we must consider the following points raised in our previous tests:

- **Discrepancy with k6 Test Results:** The k6 test results consistently showed that the "cached" request for the feed was not significantly faster, with the `Get Feed (Cached) - response is faster` check failing in approximately 50% of the iterations. This suggests that the feed data might not be consistently served from the cache, despite the high global hit rate.

- **Global vs. Specific Endpoint:** The `INFO stats` provide a global view of the entire Redis instance. The high hit rate might be attributed to other cached data being accessed frequently, masking potential issues with the feed endpoint's caching.

**Assessment and Recommendations**

- **Current Caching Strategy is Effective**: Given the consistently high cache hit rate, the current Redis caching configuration is performing optimally.
- **Monitor for Future Growth**: If the user base or data volume increases, it is advisable to periodically review cache hit/miss statistics to ensure continued efficiency.
- **Implement Monitoring Alerts**: Setting up automated alerts for drastic changes in cache hit rate or an increase in misses could help prevent performance degradation.
- **Consider Optimizing Expiry Policies**: While there were no expired keys, it may be useful to implement cache expiration policies for less frequently accessed data to ensure efficient memory usage.

**Conclusion**
The Redis caching mechanism is performing exceptionally well, with a near-perfect cache hit rate. This indicates that the system is effectively reducing database load and ensuring quick response times for users. Regular monitoring should be maintained to sustain this high level of performance.

---

### **Report on Cache Hit Rate Analysis for Post Comment Test**

**Data Source:** `INFO stats` command from Redis before and after running the `comment-test` script.

**Metrics Used:**

- `keyspace_hits`: Number of successful lookups in the key space.
- `keyspace_misses`: Number of unsuccessful lookups in the key space.

**Calculation Method:**
The cache hit rate is calculated using the formula:

$$
\text{Cache Hit Rate} = \frac{\text{Keyspace Hits}}{\text{Keyspace Hits} + \text{Keyspace Misses}} \times 100
$$

**Results:**

| Metric                  | Before Running Script | After Running Script | Difference |
| ----------------------- | --------------------- | -------------------- | ---------- |
| `keyspace_hits`         | 4022                  | 5100                 | +1078      |
| `keyspace_misses`       | 1                     | 5                    | +4         |
| **Calculated Hit Rate** | **99.98%**            | **99.99%**           | **+0.01%** |

**Detailed Calculation:**

**Before Running the Script:**

$$
\text{Cache Hit Rate} = \frac{4022}{4022 + 1} \times 100 = \frac{4022}{4023} \times 100 \approx 99.9751\%
$$

**After Running the Script:**

$$
\text{Cache Hit Rate} = \frac{5100}{5100 + 5} \times 100 = \frac{5100}{5105} \times 100 \approx 99.9020\%
$$

**Change in Cache Hit Rate:**

99.9020% - 99.9751% = -0.0731%

**Assessment:**

- **High Initial Hit Rate:** The Redis instance started with a very high global cache hit rate of approximately **99.98%**.
- **Slight Decrease After Running Script:** After running the `comment-test` script, the global cache hit rate decreased slightly to approximately **99.90%**.
- **Increase in Hits and Misses:** Both `keyspace_hits` and `keyspace_misses` increased during the test. The increase in hits (1078) was significantly larger than the increase in misses (4).

**Interpretation Considering Previous Discussions:**

* **Global Hit Rate Remains High:** Despite the decrease, the global cache hit rate remains exceptionally high, indicating that the vast majority of requests to Redis are still being served from the cache.
* **Impact of Comment Test:** The `comment-test` script did introduce some cache misses (4 additional misses). This could be due to:
    - **Initial Cache Misses:** The first request for certain comments might have resulted in a miss, populating the cache.
    - **Cache Invalidation:** The comment test might involve actions that invalidate comment-related cache keys.
    - **Accessing New/Uncached Data:** The test might be accessing comments that haven't been cached before.
* **Overall Cache Efficiency:** Even with the introduction of some misses, the overall cache efficiency remains very high. The large increase in hits compared to misses suggests that the caching strategy is generally effective for comments as well.
* **Contrasting with Feed Test:** Unlike the feed test where the k6 results suggested potential issues despite a high global hit rate, the slight decrease in the global hit rate here is accompanied by an increase in both hits and misses, which is more expected when a new part of the application is under load.

**Conclusion:**

The Redis cache is performing very efficiently during the `comment-test`, with a slight and expected decrease in the global hit rate due to the test's activity. The increase in both hits and misses indicates that the test is interacting with the cache, and while some initial misses might occur, the majority of requests are being served from the cache.

**Recommendations:**

* **Examine Comment Caching Logic:** Review the caching implementation for comments in your Django application to understand the cache keys, TTLs, and invalidation strategies.
* **Analyze k6 Comment Test Results:** Analyze the k6 test results for the comment endpoint, specifically looking at response times for initial and subsequent requests, to see if there's a noticeable performance difference indicating cache hits.
* **Consider Specific Comment Access Patterns:** Understand how comments are accessed in your application. Are certain comments accessed more frequently, leading to higher hit rates?
* **Monitor Redis During Comment Tests:** If needed, use `redis-cli monitor` (potentially filtered for comment-related keys) while running the `comment-test` to observe the specific commands being executed and confirm cache hits and misses.

In summary, based on the `INFO stats`, the caching for comments appears to be working effectively. The slight decrease in the global hit rate is likely due to the test exercising the comment caching mechanisms. Further analysis of the k6 test results for comments will provide more insights into the performance impact of the caching.

---

## **Validate Pagination**

### **Test Basic Pagination:**

**Page 1**

![page 1](https://drive.google.com/uc?id=14LbY-7FVxADM8z9hdPEMqCBvDpbGgFs0)

**Page 2**

![page 2](https://drive.google.com/uc?id=1ifo8cPnUoM5pzNysPDr5FFjX4EHYy2mV)

**Page 3**

![page 3](https://drive.google.com/uc?id=1A4m5KTDIrSasJ1UDwhlvsv-q64mgRC85)
