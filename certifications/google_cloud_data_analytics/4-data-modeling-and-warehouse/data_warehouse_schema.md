# 🏗️ Data Warehouse Schema Design
Tables: storage_perf, user_region_map, perf_daily_summary  
- Partitioned by event_time  
- Clustered on device_type, region
- Includes lifecycle rules for staging tables
