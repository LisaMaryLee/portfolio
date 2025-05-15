-- Use BQ's EXPLAIN to validate index usage
EXPLAIN
SELECT * FROM storage_perf
WHERE device_type = 'ssd'
AND latency_ms > 25;
