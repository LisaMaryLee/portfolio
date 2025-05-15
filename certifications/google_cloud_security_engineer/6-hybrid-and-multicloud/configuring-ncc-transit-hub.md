# Configuring Network Connectivity Center as a Transit Hub

**Course:** Networking in Google Cloud  
**Module:** Network Connectivity Center  
**Completed by:** Lisa Mary Lee  
**Date:** May 15, 2025

---

## 🗺️ Overview

This lab guides you through the configuration of Network Connectivity Center (NCC) to establish a transit hub for routing traffic between two remote branch offices simulated using VPCs in different regions.

---

## 🎯 Objectives

- Create a hub VPC: `vpc-transit`
- Create two remote branch VPCs: `vpc-a` and `vpc-b`
- Configure HA VPN tunnels and Cloud Routers
- Create NCC hub and spokes using VPN tunnels
- Deploy VMs and test end-to-end connectivity

---

## 🏗️ Infrastructure Setup

### 1. Delete Default Network

```bash
gcloud compute networks delete default
```

### 2. Create Transit VPC

```bash
gcloud compute networks create vpc-transit     --subnet-mode=custom     --bgp-routing-mode=global
```

### 3. Create Branch Office VPCs

```bash
# VPC A
gcloud compute networks create vpc-a --subnet-mode=custom
gcloud compute networks subnets create vpc-a-sub1-use4     --network=vpc-a     --region=us-east4     --range=10.20.10.0/24

# VPC B
gcloud compute networks create vpc-b --subnet-mode=custom
gcloud compute networks subnets create vpc-b-sub1-usw2     --network=vpc-b     --region=us-west2     --range=10.20.20.0/24
```

---

## 🌐 VPN & Cloud Router Configuration

### 4. Create Cloud Routers

```bash
# Transit VPC Routers
gcloud compute routers create cr-vpc-transit-use4-1     --network=vpc-transit --region=us-east4 --asn=65000
gcloud compute routers create cr-vpc-transit-usw2-1     --network=vpc-transit --region=us-west2 --asn=65000

# VPC A Router
gcloud compute routers create cr-vpc-a-use4-1     --network=vpc-a --region=us-east4 --asn=65001

# VPC B Router
gcloud compute routers create cr-vpc-b-usw2-1     --network=vpc-b --region=us-west2 --asn=65002
```

### 5. Create VPN Gateways

Create HA VPN gateways for all 3 VPCs using the UI or:

```bash
# Example for VPC Transit
gcloud compute vpn-gateways create vpc-transit-gw1-use4     --network=vpc-transit --region=us-east4
```

Repeat for:
- `vpc-transit-gw1-usw2` in `vpc-transit`
- `vpc-a-gw1-use4` in `vpc-a`
- `vpc-b-gw1-usw2` in `vpc-b`

---

## 🔁 Establishing HA VPN Tunnels with BGP

### 6. Transit ↔ VPC A

Establish tunnels:
- `transit-to-vpc-a-tu1` & `tu2`
- `vpc-a-to-transit-tu1` & `tu2`

Use BGP IPs:
- Tunnel 1: 169.254.1.1 ↔ 169.254.1.2
- Tunnel 2: 169.254.1.5 ↔ 169.254.1.6

Pre-shared key: `gcprocks`

---

### 7. Transit ↔ VPC B

Establish tunnels:
- `transit-to-vpc-b-tu1` & `tu2`
- `vpc-b-to-transit-tu1` & `tu2`

Use BGP IPs:
- Tunnel 1: 169.254.1.9 ↔ 169.254.1.10
- Tunnel 2: 169.254.1.13 ↔ 169.254.1.14

---

## 🧠 Network Connectivity Center Configuration

### 8. Enable API

```bash
gcloud services enable networkconnectivity.googleapis.com
```

### 9. Create NCC Hub and Spokes

```bash
gcloud alpha network-connectivity hubs create transit-hub     --description=Transit_hub

gcloud alpha network-connectivity spokes create bo1     --hub=transit-hub --description=branch_office1     --vpn-tunnel=transit-to-vpc-a-tu1,transit-to-vpc-a-tu2     --region=us-east4

gcloud alpha network-connectivity spokes create bo2     --hub=transit-hub --description=branch_office2     --vpn-tunnel=transit-to-vpc-b-tu1,transit-to-vpc-b-tu2     --region=us-west2
```

---

## 💻 Deploy VMs and Test

### 10. Create Firewall Rules

Allow SSH & ICMP in both VPCs:

```bash
gcloud compute firewall-rules create fw-a     --network=vpc-a --allow=tcp:22,icmp

gcloud compute firewall-rules create fw-b     --network=vpc-b --allow=tcp:22,icmp
```

### 11. Create VMs

VM in `vpc-a`:
- Name: `vpc-a-vm-1`
- Subnet: `vpc-a-sub1-use4`

VM in `vpc-b`:
- Name: `vpc-b-vm-1`
- Subnet: `vpc-b-sub1-usw2`

### 12. Test Connectivity

SSH into `vpc-a-vm-1` and ping:

```bash
ping -c 5 <internal-ip-of-vpc-b-vm-1>
```

Expect successful ping replies.

---

## ✅ Summary

You configured NCC with HA VPN spokes and validated cross-VPC communication between simulated branch offices using Google Cloud’s backbone.

---

**Reference Commands Index**
- `gcloud compute networks create`
- `gcloud compute routers create`
- `gcloud compute vpn-gateways create`
- `gcloud alpha network-connectivity hubs create`
- `gcloud alpha network-connectivity spokes create`
- `gcloud compute firewall-rules create`
- `ping`
