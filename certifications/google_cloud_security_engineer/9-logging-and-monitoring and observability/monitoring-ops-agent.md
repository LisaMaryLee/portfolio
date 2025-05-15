# 🛠️ Monitoring a Compute Engine by using Ops Agent

**Lab Duration:** 1 hour  
**Difficulty:** Introductory  
**Cost:** No cost  
**Lab Platform:** Google Cloud Skills Boost (Qwiklabs)  
**Date:** May 15, 2025

---

## ✅ Objectives

In this lab, you will learn how to:

- Create a Compute Engine VM instance.
- Install an Apache Web Server.
- Install and configure the Ops Agent.
- Generate traffic and view metrics on the Apache dashboard.
- Create and test an alerting policy.

---

## 🧪 Task 1: Create a Compute Engine VM Instance

- **Name:** `quickstart-vm`
- **Region/Zone:** As specified in lab
- **Series:** E2
- **Machine Type:** e2-small
- **Boot Disk:** Debian GNU/Linux 12 (bookworm)
- **Firewall:** Allow HTTP & HTTPS traffic

---

## 🌐 Task 2: Install Apache Web Server

```bash
sudo apt-get update
sudo apt-get install apache2 php7.0
```

Visit: `http://EXTERNAL_IP`

---

## ⚙️ Task 3: Install and Configure the Ops Agent

```bash
curl -sSO https://dl.google.com/cloudagents/add-google-cloud-ops-agent-repo.sh
sudo bash add-google-cloud-ops-agent-repo.sh --also-install
```

Create config:

```bash
sudo tee /etc/google-cloud-ops-agent/config.yaml > /dev/null << EOF
metrics:
  receivers:
    apache:
      type: apache
  service:
    pipelines:
      apache:
        receivers: [apache]
logging:
  receivers:
    apache_access:
      type: apache_access
    apache_error:
      type: apache_error
  service:
    pipelines:
      apache:
        receivers: [apache_access, apache_error]
EOF

sudo service google-cloud-ops-agent restart
```

---

## 📊 Task 4: Generate Traffic and View Metrics

```bash
timeout 120 bash -c -- 'while true; do curl localhost; sleep $((RANDOM % 4)) ; done'
```

- Go to: **Monitoring > Dashboards > Apache Overview**

---

## 🚨 Task 5: Create an Alerting Policy

1. **Notification Channel:** Email
2. **Metric:** `workload/apache.traffic`
3. **Trigger:** Above 4000 KiB/s (rate, 1min)
4. **Alert Name:** `Apache traffic above threshold`

---

## 🧪 Task 6: Test the Alerting Policy

```bash
timeout 120 bash -c -- 'while true; do curl localhost; sleep $((RANDOM % 4)) ; done'
```

- Wait for threshold breach → Email alert

---

## 🏁 Task 7: Review

You installed the Ops Agent, configured monitoring for Apache, and validated alerting behavior on a GCE VM using Google Cloud Monitoring.

