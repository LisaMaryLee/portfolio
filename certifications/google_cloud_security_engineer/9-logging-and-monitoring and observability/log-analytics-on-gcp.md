# 🧪 Log Analytics on Google Cloud

**Course:** Logging in Google Cloud  
**Lab:** Log Analytics on Google Cloud  
**Completed by:** Lisa Mary Lee  
**Date:** May 15, 2025

---

## 🎯 Objectives

- Use Cloud Logging effectively on GKE
- Build and run queries using log analytics

---

## 🛠️ Task 1: Infrastructure Setup

- Set zone using `gcloud config set compute/zone`
- Verified GKE cluster `day2-ops` is in `RUNNING` state
- Acquired cluster credentials:  
  `gcloud container clusters get-credentials day2-ops --region <region>`
- Verified nodes with `kubectl get nodes`

---

## 🚀 Task 2: Deploy the Application

- Cloned repo:  
  `git clone https://github.com/GoogleCloudPlatform/microservices-demo.git`
- Applied Kubernetes manifests:  
  `kubectl apply -f release/kubernetes-manifests.yaml`
- Confirmed pods are `Running`
- Retrieved external IP and confirmed frontend accessibility
- Demo app URL: `http://<EXTERNAL_IP>`

---

## 🪵 Task 3: Manage Log Buckets

### ✅ Upgraded Existing Bucket
- Upgraded `Default` log bucket for Log Analytics

### ✅ Created New Log Bucket
- Name: `day2ops-log`
- Linked BigQuery dataset: `day2ops_log`

### ✅ Created Sink
- Name: `day2ops-sink`
- Filter: `resource.type="k8s_container"`
- Routed logs into `day2ops-log` bucket

---

## 🔍 Task 4: Log Analysis

### 🐞 Recent Error Logs
```sql
SELECT TIMESTAMP, JSON_VALUE(resource.labels.container_name) AS container, json_payload
FROM `PROJECT_ID.global.day2ops-log._AllLogs`
WHERE severity="ERROR"
  AND json_payload IS NOT NULL
ORDER BY 1 DESC
LIMIT 50
```

### 📊 Latency Metrics (Frontend Service)
```sql
SELECT hour, MIN(took_ms) AS min, MAX(took_ms) AS max, AVG(took_ms) AS avg
FROM (
  SELECT FORMAT_TIMESTAMP("%H", timestamp) AS hour,
         CAST(JSON_VALUE(json_payload, '$."http.resp.took_ms"') AS INT64) AS took_ms
  FROM `PROJECT_ID.global.day2ops-log._AllLogs`
  WHERE timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)
    AND json_payload IS NOT NULL
    AND SEARCH(labels, "frontend")
    AND JSON_VALUE(json_payload.message) = "request complete"
)
GROUP BY 1
ORDER BY 1
```

### 🛍️ Product Page Visits (L9ECAV7KIM)
```sql
SELECT count(*)
FROM `PROJECT_ID.global.day2ops-log._AllLogs`
WHERE text_payload LIKE "GET %/product/L9ECAV7KIM %"
  AND timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)
```

### 💳 Checkout Sessions
```sql
SELECT JSON_VALUE(json_payload.session), COUNT(*)
FROM `PROJECT_ID.global.day2ops-log._AllLogs`
WHERE JSON_VALUE(json_payload['http.req.method']) = "POST"
  AND JSON_VALUE(json_payload['http.req.path']) = "/cart/checkout"
  AND timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)
GROUP BY JSON_VALUE(json_payload.session)
```

---

## ✅ Lab Complete

- Deployed GKE app with microservices
- Managed log buckets and routing
- Executed Log Analytics queries in BigQuery

