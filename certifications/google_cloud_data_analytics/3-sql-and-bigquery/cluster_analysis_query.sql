-- Cluster performance for comparative regional insight
SELECT region, COUNT(*) AS samples, AVG(latency_ms) AS avg_latency
FROM storage_perf
GROUP BY region
ORDER BY avg_latency ASC;
