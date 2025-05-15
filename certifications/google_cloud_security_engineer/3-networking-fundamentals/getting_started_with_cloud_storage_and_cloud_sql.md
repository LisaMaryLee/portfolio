# ☁️ Getting Started with Cloud Storage and Cloud SQL

---

## 🎯 Objectives

In this lab, you will:

- Create a Cloud Storage bucket and upload an image
- Create and configure a Cloud SQL instance
- Deploy a Compute Engine VM with a LAMP stack (Apache, PHP, MySQL)
- Connect the web server to Cloud SQL using PHP
- Display an image from Cloud Storage in a web application

---

## 🛠️ Lab Tasks

### Task 1: Sign in to Google Cloud Console

- Use temporary lab credentials provided by Qwiklabs/Coursera
- Accept terms, avoid linking to personal accounts
- Use Incognito mode to prevent credential conflicts

---

### Task 2: Deploy a Web Server VM

- Name: `bloghost`
- OS: Debian GNU/Linux 12 (bookworm)
- Install: Apache, PHP, php-mysql via startup script
- Enable HTTP firewall rule
- Confirm VM IP addresses

---

### Task 3: Create Cloud Storage Bucket

- Bucket name: Use `DEVSHELL_PROJECT_ID`
- Region: US / EU / ASIA
- Upload: `my-excellent-blog.png`
- Make object public using `gsutil acl`

```bash
gcloud storage cp gs://cloud-training/gcpfci/my-excellent-blog.png my-excellent-blog.png
gcloud storage cp my-excellent-blog.png gs://$DEVSHELL_PROJECT_ID/
gsutil acl ch -u allUsers:R gs://$DEVSHELL_PROJECT_ID/my-excellent-blog.png
```

---

### Task 4: Create Cloud SQL Instance

- Engine: MySQL (Enterprise > Sandbox)
- Instance ID: `blog-db`
- Create user: `blogdbuser`
- Configure authorized network: `bloghost` external IP with `/32` mask
- Copy SQL public IP

---

### Task 5: Connect App to Cloud SQL

- Edit `/var/www/html/index.php`:
  - Replace `CLOUDSQLIP` with SQL instance public IP
  - Replace `DBPASSWORD` with your defined SQL password
- Validate by visiting: `http://[VM_EXTERNAL_IP]/index.php`
- Expect: `Connected successfully` message

---

### Task 6: Use Cloud Storage Image

- Insert `<img src='https://storage.googleapis.com/[bucket]/my-excellent-blog.png'>` in `index.php`
- Reload web app to see image and blog header

---

## ✅ Validation Checks

- [x] Deployed web server VM and connected to it via SSH
- [x] Created and accessed Cloud Storage image publicly
- [x] Connected Compute Engine to Cloud SQL instance
- [x] Displayed banner image from Cloud Storage in browser

---

## 🧠 Key Concepts

- Cloud Storage ACL and public access
- Cloud SQL configuration and IP-based network authorization
- Connecting PHP apps to Cloud SQL using PDO
- Using metadata startup scripts in VM provisioning

---

## 🗂️ Repository Placement

```
google_cloud_security_specialization/
└── 3-data-protection-and-access-control/
    └── getting_started_with_cloud_storage_and_cloud_sql.md
```

---

© 2025 Lisa Mary Lee – All lab steps based on Coursera Security in Google Cloud coursework.