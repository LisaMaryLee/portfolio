
# Configuring and Viewing Cloud Audit Logs

**Lab Type**: Hands-on Lab  
**Duration**: 1 hour 30 minutes  
**Level**: Introductory

## 📝 Overview

In this lab, you will investigate **Cloud Audit Logs**, which help you answer **"who did what, where, and when"** in your Google Cloud environment.

Cloud Audit Logs includes:
- **Admin Activity logs**
- **Data Access logs**

---

## 🎯 Objectives

- View audit logs in the **Activity** page
- View and filter audit logs in **Cloud Logging**
- Retrieve log entries with **gcloud**
- Export audit logs to **BigQuery**

---

## 🚀 Task 1: Enable Data Access Audit Logs

1. Open Cloud Shell.
2. Export current IAM policy:
   ```bash
   gcloud projects get-iam-policy $DEVSHELL_PROJECT_ID --format=json > policy.json
   ```
3. Edit `policy.json` and insert after first `{`:
   ```json
   "auditConfigs": [
     {
       "service": "allServices",
       "auditLogConfigs": [
         { "logType": "ADMIN_READ" },
         { "logType": "DATA_READ" },
         { "logType": "DATA_WRITE" }
       ]
     }
   ],
   ```
4. Apply the updated policy:
   ```bash
   gcloud projects set-iam-policy $DEVSHELL_PROJECT_ID policy.json
   ```

---

## ⚙️ Task 2: Generate Account Activity

```bash
gcloud storage buckets create gs://$DEVSHELL_PROJECT_ID
echo "this is a sample file" > sample.txt
gcloud storage cp sample.txt gs://$DEVSHELL_PROJECT_ID
gcloud compute networks create mynetwork --subnet-mode=auto
gcloud compute instances create default-us-vm --machine-type=e2-micro --zone=ZONE --network=mynetwork
gcloud storage rm -r gs://$DEVSHELL_PROJECT_ID
```

---

## 📖 Task 3: View Admin Activity Logs

**In Logs Explorer**:
1. Navigate to: Logging > Logs Explorer.
2. Query:
   ```
   logName = ("projects/PROJECT_ID/logs/cloudaudit.googleapis.com%2Factivity")
   ```
3. Use the **Show matching entries** option for `storage.googleapis.com` and `storage.buckets.delete`.
4. Inspect `authenticationInfo.principalEmail` to see who deleted the bucket.

**With gcloud**:
```bash
gcloud logging read "logName=projects/$DEVSHELL_PROJECT_ID/logs/cloudaudit.googleapis.com%2Factivity AND protoPayload.serviceName=storage.googleapis.com AND protoPayload.methodName=storage.buckets.delete"
```

---

## 💾 Task 4: Export Logs

1. Go to **Logs Explorer**.
2. Filter logs as:
   ```
   logName = ("projects/PROJECT_ID/logs/cloudaudit.googleapis.com%2Factivity")
   ```
3. Create Sink:
   - Name: `AuditLogsExport`
   - Service: `BigQuery`
   - Dataset: `auditlogs_dataset`
4. Run more activity to populate logs:
   ```bash
   gcloud storage buckets create gs://$DEVSHELL_PROJECT_ID
   gcloud storage buckets create gs://$DEVSHELL_PROJECT_ID-test
   echo "this is another sample file" > sample2.txt
   gcloud storage cp sample.txt gs://$DEVSHELL_PROJECT_ID-test
   gcloud compute instances delete --zone=ZONE --delete-disks=all default-us-vm
   gcloud storage rm -r gs://$DEVSHELL_PROJECT_ID
   gcloud storage rm -r gs://$DEVSHELL_PROJECT_ID-test
   ```

---

## 📊 Task 5: Analyze Logs in BigQuery

**Query deleted VMs**:
```sql
SELECT
  timestamp,
  resource.labels.instance_id,
  protopayload_auditlog.authenticationInfo.principalEmail,
  protopayload_auditlog.resourceName,
  protopayload_auditlog.methodName
FROM
  `auditlogs_dataset.cloudaudit_googleapis_com_activity_*`
WHERE
  PARSE_DATE('%Y%m%d', _TABLE_SUFFIX) BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY) AND CURRENT_DATE()
  AND resource.type = "gce_instance"
  AND operation.first IS TRUE
  AND protopayload_auditlog.methodName = "v1.compute.instances.delete"
ORDER BY timestamp
LIMIT 1000
```

**Query deleted buckets**:
```sql
SELECT
  timestamp,
  resource.labels.bucket_name,
  protopayload_auditlog.authenticationInfo.principalEmail,
  protopayload_auditlog.resourceName,
  protopayload_auditlog.methodName
FROM
  `auditlogs_dataset.cloudaudit_googleapis_com_activity_*`
WHERE
  PARSE_DATE('%Y%m%d', _TABLE_SUFFIX) BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY) AND CURRENT_DATE()
  AND resource.type = "gcs_bucket"
  AND protopayload_auditlog.methodName = "storage.buckets.delete"
ORDER BY timestamp
LIMIT 1000
```

---

## ✅ Congratulations

You successfully:
- Enabled and viewed audit logs
- Filtered and retrieved activity with `gcloud`
- Exported logs to BigQuery
- Queried logs to analyze admin activities

---
