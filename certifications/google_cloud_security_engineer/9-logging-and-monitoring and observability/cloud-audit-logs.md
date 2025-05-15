# Cloud Audit Logs

**Course:** Cloud Operations and Logging  
**Lab Title:** Cloud Audit Logs  
**Duration:** 1 hour  
**Level:** Intermediate  
**Date:** May 15, 2025  

---

## 🧠 Objectives

In this lab, you learn how to:

- Enable data access logs on Cloud Storage.
- Generate admin and data access activity.
- View Audit logs.

---

## 🛠️ Task 1: Enable Data Access Logs on Cloud Storage

1. Go to **IAM & Admin > Audit Logs**.
2. Locate **Google Cloud Storage**.
3. Enable the following **Log Types**:
   - Admin Read
   - Data Read
   - Data Write
4. Click **Save**.

✅ *Checkpoint:* You enabled data access logs for Cloud Storage.

---

## 📦 Task 2: Generate Admin and Data Access Activity

In **Cloud Shell**, run the following to simulate activity:

```bash
gcloud storage buckets create gs://$DEVSHELL_PROJECT_ID
gcloud storage ls
echo "Hello World!" > sample.txt
gcloud storage cp sample.txt gs://$DEVSHELL_PROJECT_ID
gcloud storage ls gs://$DEVSHELL_PROJECT_ID
```

Create a custom VPC and VM:

```bash
gcloud compute networks create mynetwork --subnet-mode=auto
gcloud compute instances create default-us-vm \
  --zone=ZONE --network=mynetwork \
  --machine-type=e2-medium
```

Delete the Cloud Storage bucket:

```bash
gcloud storage rm -r gs://$DEVSHELL_PROJECT_ID
```

✅ *Checkpoint:* Admin and data access activity generated.

---

## 🔍 Task 3: Viewing Audit Logs

### In Logs Explorer

1. Navigate to **Logging > Logs Explorer**.
2. Enable **Show Query**.
3. Select log name:  
   `cloudaudit.googleapis.com/activity`
4. Filter to **GCS Bucket** entries.
5. Locate and expand the bucket delete entry:
   - View `protoPayload.authenticationInfo` to see the user.
6. Switch log name to:  
   `cloudaudit.googleapis.com/data_access`
7. View data read/write operations.

### Using Cloud SDK

```bash
gcloud logging read \
"logName=projects/$DEVSHELL_PROJECT_ID/logs/cloudaudit.googleapis.com%2Fdata_access"
```

✅ *Checkpoint:* Viewed and filtered Admin Activity and Data Access logs.

---

## 🎉 Congratulations!

In this lab, you:

- Enabled Cloud Storage data access logs.
- Generated activity logs.
- Viewed audit trails in Logs Explorer and the SDK.

You’re now more confident in identifying **"who did what, when, and where"** using Cloud Audit Logs!
