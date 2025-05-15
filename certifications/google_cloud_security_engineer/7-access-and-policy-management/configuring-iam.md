
# Configuring IAM

**Course:** Identity and Access Management (IAM) on Google Cloud  
**Module:** Full IAM Role Lifecycle  

---

## 🛠️ Objectives

- Use IAM to implement access control
- Restrict access to specific features/resources
- Use predefined roles
- Create and manage custom IAM roles
- Modify custom roles

---

## ✅ Tasks Summary

### Task 1: Sign in with Two User Accounts
- Open Chrome in Incognito
- Sign in as Username 1 and Username 2 from Qwiklabs
- Username 1: Project Owner  
- Username 2: Project Viewer

### Task 2: Explore IAM Console
- IAM > Users:
  - Username 1: Owner (full permissions)
  - Username 2: Viewer (read-only)
- Username 2 cannot change roles

### Task 3: Prepare Access Test Resource
- Create GCS bucket and upload `sample.txt`
- Username 2 can list but **not upload** (no `storage.objects.create`)

### Task 4: Remove Project Access
- Removed Viewer role from Username 2
- Confirmed denied access to GCS and Compute Engine

### Task 5: Add Storage Access
- Assigned `roles/storage.objectViewer` to Username 2
- Verified read access to GCS via `gcloud storage ls`

---

## 🧩 Custom Role Creation

### GUI-Based: Privacy Reviewer
```yaml
title: Privacy Reviewer
description: Custom role to perform data reviews
stage: ALPHA
includedPermissions:
  - storage.buckets.list
  - storage.objects.list
  - storage.objects.get
  - spanner.databases.get
  - spanner.databases.list
  - bigtable.tables.get
  - bigtable.tables.list
  - bigtable.tables.readRows
```

### CLI-Based: App Viewer
```bash
nano role.yaml
```
```yaml
title: App Viewer
description: Custom role to view apps
stage: ALPHA
includedPermissions:
  - compute.instances.get
  - compute.instances.list
  - appengine.versions.get
  - appengine.versions.list
```
```bash
gcloud iam roles create app_viewer --project $DEVSHELL_PROJECT_ID --file role.yaml
```

---

## 🔄 Custom Role Lifecycle

### Modify Role
```bash
gcloud iam roles update app_viewer --project $DEVSHELL_PROJECT_ID --file update-role.yaml
```

### Disable Role
```bash
gcloud iam roles update app_viewer --project $DEVSHELL_PROJECT_ID --stage DISABLED
```

### Delete Role
```bash
gcloud iam roles delete app_viewer --project $DEVSHELL_PROJECT_ID
```

### Undelete Role
```bash
gcloud iam roles undelete app_viewer --project $DEVSHELL_PROJECT_ID
```

---

## 🧾 Review
- IAM allows for precise access control.
- Custom roles provide flexibility but require manual maintenance.
- Predefined roles are best for most use cases.

---

© 2025 Google LLC — All rights reserved.
