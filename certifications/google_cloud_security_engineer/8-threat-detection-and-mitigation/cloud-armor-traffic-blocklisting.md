# Configuring Traffic Blocklisting with Google Cloud Armor

**Course:** Google Cloud Security Engineer  
**Module:** 8 - Threat Detection and Mitigation  
**Completed by:** Lisa Mary Lee  
**Date:** May 15, 2025

---

## 🧠 Overview

This lab demonstrates how to use **Google Cloud Armor** to apply IP blocklists on a global Application Load Balancer. This limits or denies access to services from malicious IP addresses as early as possible — at the edge of Google’s network.

---

## 🎯 Objectives

- Verify deployment of a global Application Load Balancer.
- Create a VM and test load balancer access.
- Use Google Cloud Armor to blocklist traffic based on IP.
- View and analyze Cloud Armor logs for visibility and auditing.

---

## 🛠️ Task 1: Verify the Load Balancer

```bash
gcloud compute backend-services get-health web-backend --global
gcloud compute forwarding-rules describe web-rule --global
```

- Wait until all three backend instances are reported `HEALTHY`.
- Access `http://<IP_ADDRESS>` in a browser or via:

```bash
while true; do curl -m1 <IP_ADDRESS>; done
```

---

## 💻 Task 2: Create Test VM

1. Create a VM:
   - Name: `access-test`
   - Region/Zone: any available
   - Machine type: default (e2-micro)

2. SSH into VM and test:
```bash
curl -m1 <IP_ADDRESS>
```

---

## 🛡️ Task 3: Configure Cloud Armor Policy

### 1. Get the external IP of `access-test`.

### 2. Create a Cloud Armor policy:
- Name: `blocklist-access-test`
- Default rule: Allow
- Add Rule:
  - Mode: Basic
  - Match: `<ACCESS-TEST-IP>`
  - Action: Deny
  - Response: 404
  - Priority: 1000

### 3. Apply to target:
- Backend service: `web-backend`

### 4. Test access from VM:
```bash
curl -m1 <IP_ADDRESS>
```

> Should return `404 Not Found`.

---

## 📊 Task 4: Review Cloud Armor Logs

1. Go to:
   - `Network Security > Cloud Armor policies > blocklist-access-test > Logs`

2. Click "View policy logs"

3. Look for 404 responses from `access-test` VM's IP.

---

## ✅ Lab Completed

You have:
- Applied and validated IP-based traffic filtering using Cloud Armor.
- Demonstrated layered defense on an Application Load Balancer.

---  
**Next Step:** Try the follow-up lab: *Securing your Network with Cloud Armor*
