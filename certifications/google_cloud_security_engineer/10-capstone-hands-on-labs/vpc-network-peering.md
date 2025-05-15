# VPC Network Peering – Lab Summary

**Lab Duration**: 1 hour  
**Difficulty**: Intermediate  
**Lab ID**: GSP193  

---

## 🧠 Overview

VPC Network Peering allows private connectivity between VPC networks across different projects or organizations, facilitating secure, low-latency, and cost-effective communication.

---

## ✅ Objectives

- Create a custom network in two separate projects
- Set up VPC Network Peering between those networks
- Test VM-to-VM connectivity over the peered network

---

## 🛠️ Setup Steps

### 1. Create Custom Networks in Two Projects

#### In Project A:
```bash
gcloud config set project PROJECT_ID_1
gcloud compute networks create network-a --subnet-mode custom
gcloud compute networks subnets create network-a-subnet --network network-a --range 10.0.0.0/16 --region REGION_1
gcloud compute instances create vm-a --zone ZONE_1 --network network-a --subnet network-a-subnet --machine-type e2-small
gcloud compute firewall-rules create network-a-fw --network network-a --allow tcp:22,icmp
```

#### In Project B:
```bash
gcloud config set project PROJECT_ID_2
gcloud compute networks create network-b --subnet-mode custom
gcloud compute networks subnets create network-b-subnet --network network-b --range 10.8.0.0/16 --region REGION_2
gcloud compute instances create vm-b --zone ZONE_2 --network network-b --subnet network-b-subnet --machine-type e2-small
gcloud compute firewall-rules create network-b-fw --network network-b --allow tcp:22,icmp
```

---

### 2. Set Up VPC Peering

#### From Project A (peer-ab):
- Go to **Networking > VPC Network Peering**
- Click **Create connection**
- Name: `peer-ab`
- Peering with: **Project B** / `network-b`

#### From Project B (peer-ba):
- Go to **Networking > VPC Network Peering**
- Click **Create connection**
- Name: `peer-ba`
- Peering with: **Project A** / `network-a`

Once both ends are configured, the peering state becomes `ACTIVE`.

---

### 3. Test VM Connectivity

1. Copy `INTERNAL_IP` of `vm-a` from Project A
2. SSH into `vm-b` in Project B
3. Run:
```bash
ping -c 5 INTERNAL_IP_OF_VM_A
```

Expected result: 0% packet loss and low-latency pings, confirming successful peering.

---

## 🔁 Summary

You:
- Created two custom VPCs in different projects
- Set up VPC Network Peering between them
- Verified internal communication using ping

---

## 📚 Further Reading

- [VPC Network Peering Overview](https://cloud.google.com/vpc/docs/vpc-peering)
- [Best Practices for VPC Design](https://cloud.google.com/vpc/docs/best-practices)
