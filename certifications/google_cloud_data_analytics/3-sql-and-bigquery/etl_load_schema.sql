-- Schema used for ingestion from GCS to BigQuery
CREATE OR REPLACE TABLE storage_perf (
    device_id STRING,
    read_iops FLOAT64,
    write_iops FLOAT64,
    latency_ms FLOAT64,
    region STRING,
    event_time TIMESTAMP
);
