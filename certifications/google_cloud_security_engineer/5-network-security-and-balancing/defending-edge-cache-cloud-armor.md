# Defending Edge Cache with Cloud Armor

**Course:** Security in Google Cloud Specialization  
**Module:** Defending Edge Cache with Cloud Armor  
**Completed by:** Lisa Mary Lee  
**Date:** May 15, 2025  

---

## 🧠 Overview

In this lab, you will:
- Set up a Cloud Storage Bucket with cacheable content
- Create an edge security policy to protect the content
- Validate the edge security policy behavior

---

## 🛠️ Commands Used

### Set Project ID
```bash
export PROJECT_ID=$(gcloud config get-value project)
echo $PROJECT_ID
gcloud config set project $PROJECT_ID
```

### Download and Upload Content
```bash
wget --output-document google.png https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png
gsutil cp google.png gs://<BUCKET_NAME>
rm google.png
```

### Make Object Public
- In Console: Cloud Storage > Bucket > Object > Edit Access > Add "Public"

### Create Load Balancer
1. Console: Network services > Load balancing > Create Load Balancer
2. Select "Application Load Balancer (HTTP/HTTPS)"
3. Public facing, global external
4. Backend: Cloud Storage bucket
5. Frontend: HTTP, ephemeral IP
6. Routing rule: simple host/path rule

### Verify Load Balancer Response
```bash
curl -svo /dev/null http://<LOAD_BALANCER_IP>/google.png
for i in `seq 1 50`; do curl http://<LOAD_BALANCER_IP>/google.png; done
```

### Delete Object
- Console: Cloud Storage > Bucket > Object > Delete

### Create Edge Security Policy
```bash
# In Console:
# Network Security > Cloud Armor > Create Policy
# Name: edge-security-policy
# Type: Edge Security Policy
# Default action: Deny
# Target: Backend bucket (lb-backend-bucket)
```

### Confirm Deny Policy Works
```bash
curl -svo /dev/null http://<LOAD_BALANCER_IP>/google.png
```

### Logs Explorer Query
```text
resource.type:(http_load_balancer) AND jsonPayload.@type="type.googleapis.com/google.cloud.loadbalancing.type.LoadBalancerLogEntry" AND severity>=WARNING
```

### Remove Security Policy
- Console: Cloud Armor Policy > edge-security-policy > Remove Target

### Confirm CDN Still Delivers Cached Content
```bash
curl -svo /dev/null http://<LOAD_BALANCER_IP>/google.png
```

---

## ✅ Lab Complete

- CDN content cached and served even after source object was deleted
- Edge security policy successfully blocked unauthorized access
- Logs validated with 403 errors and policy details

