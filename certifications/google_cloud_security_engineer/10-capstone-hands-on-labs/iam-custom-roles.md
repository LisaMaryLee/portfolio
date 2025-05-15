
# IAM Custom Roles – Lab Summary

## Overview
This lab focused on creating, managing, and updating custom roles in Google Cloud IAM to enforce the principle of least privilege.

---

## ✅ Tasks Completed

### Task 1: View Available Permissions
```bash
gcloud iam list-testable-permissions //cloudresourcemanager.googleapis.com/projects/$DEVSHELL_PROJECT_ID
```

### Task 2: Get Role Metadata
```bash
gcloud iam roles describe roles/viewer
```

### Task 3: View Grantable Roles
```bash
gcloud iam list-grantable-roles //cloudresourcemanager.googleapis.com/projects/$DEVSHELL_PROJECT_ID
```

---

## 🎯 Custom Role Management

### Task 4: Create Custom Role (YAML)
```yaml
# role-definition.yaml
title: "Role Editor"
description: "Edit access for App Versions"
stage: "ALPHA"
includedPermissions:
  - appengine.versions.create
  - appengine.versions.delete
```
```bash
gcloud iam roles create editor --project $DEVSHELL_PROJECT_ID --file role-definition.yaml
```

### Task 4: Create Custom Role (Flags)
```bash
gcloud iam roles create viewer --project $DEVSHELL_PROJECT_ID \
  --title "Role Viewer" --description "Custom role description." \
  --permissions compute.instances.get,compute.instances.list --stage ALPHA
```

---

## 🔧 Role Updates

### Task 5: List Custom Roles
```bash
gcloud iam roles list --project $DEVSHELL_PROJECT_ID
```

### Task 6: Update Role with YAML
```bash
# Add storage permissions and update
gcloud iam roles update editor --project $DEVSHELL_PROJECT_ID --file new-role-definition.yaml
```

### Task 6: Update Role with Flags
```bash
gcloud iam roles update viewer --project $DEVSHELL_PROJECT_ID \
  --add-permissions storage.buckets.get,storage.buckets.list
```

---

## ⚙️ Role Lifecycle

### Task 7: Disable a Role
```bash
gcloud iam roles update viewer --project $DEVSHELL_PROJECT_ID --stage DISABLED
```

### Task 8: Delete a Role
```bash
gcloud iam roles delete viewer --project $DEVSHELL_PROJECT_ID
```

### Task 9: Restore a Role
```bash
gcloud iam roles undelete viewer --project $DEVSHELL_PROJECT_ID
```

---

## 🏁 Completion
You successfully created, updated, disabled, deleted, and restored IAM custom roles in Google Cloud.
