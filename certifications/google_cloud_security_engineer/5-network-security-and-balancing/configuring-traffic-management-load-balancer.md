**Course:** Networking in Google Cloud: Fundamentals  
**Lab:** Configuring Traffic Management with a Load Balancer  
**Completed by:** Lisa Mary Lee  
**Date:** May 15, 2025

---

### 🛠️ Lab Overview
In this lab, you created a **regional internal Application Load Balancer** to manage traffic between two managed instance groups with a blue-green deployment strategy. The load balancer was configured to route 70% of traffic to the blue deployment and 30% to the green deployment.

---

### ✅ Lab Tasks

#### 1. View Preconfigured Infrastructure
- VPC: `my-internal-app`
- Subnets: `subnet-a`, `subnet-b`
- Managed instance groups: `instance-group-1` (blue), `instance-group-2` (green)
- Firewall rules for ICMP, SSH, health checks, and LB access
- Utility VM (`utility-vm`) created for internal test access

#### 2. Configure Load Balancer
- Type: **Regional Internal Application Load Balancer**
- Proxy subnet: `my-proxy-subnet` (10.10.40.0/24)
- Backend services:
  - `blue-service`: 70% traffic → `instance-group-1`
  - `green-service`: 30% traffic → `instance-group-2`
- Routing rule using YAML `weightedBackendServices`
- Frontend IP: `10.10.30.5`

#### 3. Test Load Balancer
- Tested from `utility-vm` with:
```bash
curl 10.10.30.5
```
- Verified traffic splitting between `instance-group-1` and `instance-group-2` based on routing weights.

---

### 🧠 Key Concepts
- **Blue-green deployment**: a release management strategy to reduce downtime and risk.
- **Regional Internal ALB**: handles internal traffic within a region.
- **Routing rules**: enable fine-grained control for weighted traffic.

---

### 🧾 Reference Commands

```bash
# View internal IP response
curl 10.10.20.2
curl 10.10.30.2

# Create custom ephemeral IP on utility-vm
gcloud compute instances create utility-vm   --zone=ZONE --subnet=subnet-a --private-network-ip=10.10.20.50   --no-address

# Test Load Balancer
curl 10.10.30.5
```

---

**Status:** ✅ Completed  
**Next Lab:** Advanced Load Balancing Techniques
