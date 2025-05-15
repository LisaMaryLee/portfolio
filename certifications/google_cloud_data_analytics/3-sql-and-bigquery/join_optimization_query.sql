-- Optimize JOIN with partition filtering
SELECT a.device_id, a.read_iops, b.region
FROM storage_perf a
JOIN region_mapping b ON a.location_id = b.location_id
WHERE a.event_time BETWEEN '2024-04-01' AND '2024-04-30'
AND b.region IS NOT NULL;
