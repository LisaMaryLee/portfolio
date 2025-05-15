# 🧭 Lab: Implementing a Hub and Spoke using NCC

---

## 🧪 Lab Summary

In this lab, you implemented a **hub-and-spoke network topology** using **Network Connectivity Center (NCC)**. You verified isolated VPC connectivity, created a central hub, connected spokes, and re-tested successful interconnectivity. The Network Topology tool was also used to visualize traffic flow.

---

## 🎯 Objectives

- Deploy VMs in three isolated VPCs: `hub-vpc`, `spoke1-vpc`, and `spoke2-vpc`
- Verify that `spoke1` and `spoke2` cannot communicate
- Use **NCC** to create a hub with VPC spokes for connectivity
- Retest inter-VPC communication via the hub
- Visualize the network using the Network Topology tool

---

## 📌 Reference Commands

```bash
# Enable required APIs
gcloud services enable networkconnectivity.googleapis.com

# Create VMs
gcloud compute instances create hub-vm --zone=ZONE --network=hub-vpc
gcloud compute instances create spoke1-vm --zone=ZONE --network=spoke1-vpc
gcloud compute instances create spoke2-vm --zone=ZONE --network=spoke2-vpc

# Ping test (before hub setup - should fail)
ping <spoke2-vm-internal-ip>

# Create NCC Hub
gcloud network-connectivity hubs create my-hub

# Create NCC Spokes
gcloud network-connectivity spokes create spoke1 --hub=my-hub --location=REGION --vpc=spoke1-vpc --spoke-type=VPC
gcloud network-connectivity spokes create spoke2 --hub=my-hub --location=REGION --vpc=spoke2-vpc --spoke-type=VPC

# Ping test (after hub setup - should succeed)
ping -c 3 <spoke2-vm-internal-ip>
```

---

## 🗓️ Metadata

**Course:** Preparing for Google Cloud Certification: Cloud Security Engineer  
**Lab:** Implementing a Hub and Spoke using NCC  
**Completed by:** Lisa Mary Lee  
**Date:** May 15, 2025

