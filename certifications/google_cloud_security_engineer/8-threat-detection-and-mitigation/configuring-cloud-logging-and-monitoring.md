# Configuring and Using Cloud Logging and Cloud Monitoring

**Duration:** 1 hour 15 minutes  
**Level:** Introductory  
**Cost:** No cost  
**Lab Source:** Qwiklabs

## Objectives

In this lab, you will learn to:

- View logs using a variety of filtering mechanisms.
- Exclude log entries and disable log ingestion.
- Export logs and run reports against exported logs.
- Create and report on logging metrics.
- Use Cloud Monitoring to monitor different Google Cloud projects.
- Create a metrics dashboard.

---

## Task 1: View and Filter Logs in First Project

- Access **Logs Explorer** to identify services generating logs.
- Filter logs by:
  - Resource Type: `gce_instance`
  - Log Name: `syslog`
- Use log streaming to view live updates.

---

## Task 2: Use Log Exports

### Export GCE VM Logs to BigQuery

1. Go to **Log Router**, create a sink:
   - Name: `vm_logs`
   - Service: BigQuery
   - Dataset: `project_logs`
   - Inclusion filter: `resource.type="gce_instance"`

2. Create another sink for Load Balancer logs:
   - Name: `load_bal_logs`
   - Filter: `resource.type="http_load_balancer"`

### Verify in BigQuery:
- Go to **BigQuery > project_logs** dataset.
- Confirm log tables exist.
- Sample query:
```sql
SELECT logName, resource.type, resource.labels.zone, resource.labels.project_id
FROM `project_logs.syslog_*`
```

---

## Task 3: Create a Logging Metric

- Go to **Monitoring > Logs-based Metrics**:
  - Name: `403s`
  - Type: Counter
  - Filter:
    ```
    resource.type="gce_instance"
    log_name="projects/PROJECT_ID/logs/syslog"
    ```

---

## Task 4: Create a Monitoring Dashboard

1. Switch to Project 2 and create a **Monitoring Workspace**.
2. Add Project 1 to the workspace.
3. Create a custom dashboard with:
   - **CPU Usage** (Metric: `compute.googleapis.com/instance/cpu/usage_time`)
   - **Memory Utilization** (Metric: `agent.googleapis.com/memory/percent_used`)
   - **403s** logs-based metric

---

## Summary

You successfully:

- Viewed and filtered logs.
- Set up log exclusions and exports.
- Created BigQuery sinks and validated via SQL queries.
- Built logging metrics and integrated them into a Monitoring dashboard.
