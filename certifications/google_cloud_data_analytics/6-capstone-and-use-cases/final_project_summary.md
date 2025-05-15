# 🎓 Capstone Summary: Cloud Analyst Project

This final project simulated a cloud data analyst scenario at an enterprise company migrating storage telemetry to BigQuery.

## Scope
- Source data: 2M rows from CSV logs uploaded to GCS
- Destination: Partitioned + clustered BigQuery dataset

## Transformation SQL
```sql
-- Join telemetry with region map and enrich with derived column
SELECT
  sp.device_id,
  sp.read_iops,
  sp.write_iops,
  sp.latency_ms,
  rm.region,
  sp.event_time,
  CASE WHEN sp.latency_ms > 50 THEN 'High Latency' ELSE 'Normal' END AS latency_flag
FROM storage_perf sp
JOIN region_mapping rm
ON sp.location_id = rm.location_id
WHERE sp.event_time BETWEEN '2024-04-01' AND '2024-04-30';
```

## KPIs Tracked
- IOPS (read/write)
- Latency by device type and region
- Failed ingestion percentage

## Tools Used
- GCS, Cloud Storage Transfer, BigQuery
- SQL, Dashboard mockup (Looker Studio)
