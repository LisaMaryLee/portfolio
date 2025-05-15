# 🌐 Getting Started with VPC Networking and Google Compute Engine

**Lab Duration:** 40 minutes  
**Level:** Introductory  
**Cost:** No cost  
**Platform:** Google Cloud Skills Boost  

---

## 🧠 Objectives

In this hands-on lab, you learn how to:

- Explore the default VPC network
- Create an auto mode network with firewall rules
- Create VM instances using Compute Engine
- Explore the connectivity for VM instances

---

## 🛠️ Tasks Performed

### ✅ Task 1: Explore the Default Network

- Viewed default network subnets across all regions.
- Inspected routing rules and firewall rules.
- Deleted all default firewall rules and the network itself.
- Verified inability to launch a VM without a VPC.

### ✅ Task 2: Create a New VPC Network and Launch VMs

- Created `mynetwork` in auto mode.
- Applied standard firewall rules (ICMP, SSH, RDP, internal).
- Launched `mynet-us-vm` and `mynet-r2-vm` in different regions.

### ✅ Task 3: Explore Connectivity

- Verified SSH access and ICMP ping between instances.
- Sequentially deleted:
  - `allow-icmp` → lost external ping access.
  - `allow-custom` → lost internal ping access.
  - `allow-ssh` → lost SSH access.

### ✅ Task 4: Review

- Demonstrated the critical role of firewall rules in enabling traffic.
- Showed how network isolation works and impacts VM connectivity.

---

## 💡 Key Concepts Covered

- VPC subnets and CIDR ranges
- Google Cloud routing and firewall behavior
- Auto mode VPC setup
- Ephemeral vs. static IPs
- Inter-instance communication and firewall rule management

---

## 🗂️ File Location in Repository

```
google_cloud_data_analytics/
└── 3-sql-and-bigquery/
    └── getting_started_with_vpc_and_compute_engine.ipynb
```

---

## 👩‍💻 Author

**Lisa Mary Lee**  
💼 [LinkedIn](https://www.linkedin.com/in/lisamarylee)  
📫 lisamarylee@gmail.com

---

## 📜 License

Licensed under the [MIT License](LICENSE). Examples included are original work or course-based derivations created for educational use.
