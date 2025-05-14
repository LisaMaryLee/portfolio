-- Sample BigQuery SQL
SELECT
  device_id,
  AVG(write_latency_ms) AS avg_latency,
  COUNT(*) AS write_ops
FROM
  `project.dataset.storage_logs`
WHERE
  timestamp BETWEEN TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY) AND CURRENT_TIMESTAMP()
GROUP BY
  device_id
ORDER BY
  avg_latency DESC;
