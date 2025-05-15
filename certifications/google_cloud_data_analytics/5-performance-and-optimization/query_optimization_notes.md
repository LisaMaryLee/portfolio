# ⚙️ SQL Optimization Notes

This document captures BigQuery optimization techniques tested during the Google Cloud Data Analytics certification.

## Techniques

### 1. Use EXPLAIN to inspect query plans
```sql
EXPLAIN
SELECT device_id, latency_ms
FROM storage_perf
WHERE device_type = 'ssd'
AND latency_ms > 50;
```

### 2. Replace SELECT * with explicit columns
```sql
SELECT device_id, read_iops, region
FROM storage_perf
WHERE region = 'us-central1';
```

### 3. Apply filters early
```sql
SELECT *
FROM storage_perf
WHERE event_time > '2024-04-01'
AND device_type = 'ssd';
```

### 4. Cluster on frequently filtered columns
```sql
CREATE TABLE storage_perf_clustered
PARTITION BY DATE(event_time)
CLUSTER BY region, device_type AS
SELECT * FROM raw_perf_data;
```
