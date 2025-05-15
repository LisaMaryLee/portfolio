# 🛠️ Monitoring and Dashboarding Multiple Projects

**Course:** Google Cloud Observability  
**Lab Title:** Monitoring and Dashboarding Multiple Projects  
**Level:** Intermediate  
**Duration:** 2 hours  
**Completed by:** Lisa Mary Lee  
**Date:** May 15, 2025  

---

## 🎯 Objectives

In this lab, you will:

- Configure a dedicated monitoring project.
- Link multiple worker projects to a central metrics scope.
- Create and manage Monitoring Groups.
- Configure uptime checks.
- Build and populate a custom dashboard for metrics visibility.

---

## 🧱 Task 1: Configure the Worker Projects

- Provisioned **2 Compute Engine VMs**, one in each worker project:
  - `worker-1-server` (Zone: defined during lab)
  - `worker-2-server`
- Installed **NGINX** on both servers to serve HTTP responses.
- Allowed HTTP traffic via firewall.
- Verified default NGINX welcome page via External IP in browser.
- Captured external IPs for each VM.

---

## 📐 Task 2: Create Metrics Scope

- Switched to **Monitoring Project**.
- Accessed **Cloud Monitoring > Settings > Metric Scope**.
- Added **Worker 1** and **Worker 2** projects.
- Confirmed VM instance metrics visibility across projects.

---

## 👥 Task 3: Create and Configure Monitoring Groups

- Labeled both worker servers:
  - `component=frontend`
  - `stage=dev` (Worker 1), `stage=test` (Worker 2)
- Created **Monitoring Group**:
  - Name: `Frontend Servers`
  - Match: Tag `component=frontend`
- Created **Subgroup**:
  - Name: `Frontend Dev`
  - Match: Tag `component=frontend` AND `stage=dev`

---

## 🔍 Task 4: Create and Test Uptime Check

- Created **HTTP Uptime Check**:
  - Applied to group `Frontend Servers`
  - Path: `/`
  - Frequency: 1 minute
- Tested check (expected 200 OK).
- Simulated failure:
  - Stopped `worker-1-server` VM.
  - Observed drop in uptime metrics, alert triggered.
- Validated alerts via:
  - Uptime Check chart
  - Metric Explorer
  - Logs Explorer
  - Alerts panel

---

## 📊 Task 5: Build a Custom Dashboard

- Created dashboard: `Developer's Frontend`
- Added:
  - **Line chart:** `Dev Server Uptime`
    - Metric: `uptime_check/check_passed`
    - Filtered by `instance_id` of `worker-1-server`
  - **Line chart:** `CPU Utilization`
    - Metric: `instance/cpu/utilization`
    - Filtered by `instance_name=worker-1-server`
- Simulated load using Apache Bench from `worker-2-server`:
  ```bash
  ab -s 120 -n 100000 -c 100 $URL/
  ab -s 120 -n 500000 -c 500 $URL/
  ```
- Observed CPU utilization spikes in dashboard.

---

## ✅ Lab Complete

In this lab you:

- Centralized monitoring for multiple Google Cloud projects.
- Built meaningful groups and metrics.
- Configured uptime checks and alerts.
- Designed and validated a custom dashboard for observability.

---

**Repository Placement:**  
This lab should be stored under:  
📁 `google_cloud_observability/`  
└── 📄 `monitoring-dashboarding-multiple-projects.md`