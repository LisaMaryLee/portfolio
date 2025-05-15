**Course:** Networking in Google Cloud: Fundamentals  
**Module:** Configuring VPC Networks and Firewall Rules  

---

### 🧭 Overview

In this lab, you investigated Virtual Private Cloud (VPC) networks and created firewall rules to control access. You:

- Created both auto-mode and custom-mode VPC networks
- Deployed VM instances in these networks
- Explored default firewall rules
- Verified and tested SSH and ICMP connectivity
- Applied ingress and egress firewall rules with priorities

---

### 🛠️ Key Tasks and Outcomes

#### Task 1: Create VPC Networks and Instances
- Created `mynetwork` (auto-mode) and `privatenet` (custom-mode)
- Launched VMs in `default`, `mynetwork`, and `privatenet`
- Validated VPC modes and subnet behaviors

#### Task 2: Explore and Delete the Default Network
- Investigated default firewall rules:
  - `default-allow-ssh`, `default-allow-rdp`, etc.
- Verified that SSH worked on `default-vm-1`
- Deleted `default-vm-1` and then removed the `default` VPC

#### Task 3: Confirm Custom Networks Block Ingress by Default
- Validated SSH to `mynet-vm-1` and `mynet-vm-2` fails without firewall rules

#### Task 4: Create Custom Ingress Firewall Rules
- Created firewall rule allowing SSH from Cloud Shell IP with target tag `lab-ssh`
- Tagged `mynet-vm-1` and `mynet-vm-2` with `lab-ssh`
- Verified SSH success from Cloud Shell
- Created ICMP rule `mynetwork-ingress-allow-icmp-internal`
- Verified ping works for internal addresses but not external

#### Task 5: Set Firewall Rule Priorities
- Created DENY ICMP ingress rule with priority `500`
  - ICMP blocked
- Increased priority of DENY rule to `2000`
  - ICMP allowed due to lower priority ALLOW rule

#### Task 6: Configure Egress Firewall Rule
- Created ICMP DENY egress rule with priority `10000`
- Verified ICMP blocked due to no matching ALLOW egress rule

---

### 🔐 Concepts Practiced

- VPC modes and subnetting
- Stateful firewall rules
- Ingress vs. egress traffic
- Rule evaluation order using priorities
- Using tags for firewall targeting

---

✅ **Lab Completed Successfully**

