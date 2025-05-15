# 🌐 Lab: Configuring VPC Network Peering

---

## 🧪 Lab Summary

This lab focuses on setting up and testing **VPC network peering** in Google Cloud. It demonstrates how to establish private communication between VMs in different networks using internal IP addresses.

---

## 🎯 Objectives

- Explore connectivity between non-peered VPC networks
- Configure VPC network peering between `mynetwork` and `privatenet`
- Verify internal communication using private IPs
- Remove VPC peering and confirm de-peered state

---

## 🛠️ Key Concepts and Actions

- **VPC Peering Advantages**: Reduces latency, enhances security, and avoids public egress costs.
- **Pre-checks**: Ensured non-overlapping CIDR ranges between subnets in `mynetwork` and `privatenet`.
- **Peering Setup**:
  - Created peering from `mynetwork` ➝ `privatenet` (`peering-1-2`)
  - Created peering from `privatenet` ➝ `mynetwork` (`peering-2-1`)
  - Verified status changed to `ACTIVE`
- **Connectivity Verification**:
  - Internal ping from `mynet-us-vm` ➝ `privatenet-us-vm` successful
  - Reverse ping also successful
  - DNS resolution across networks failed (expected)
- **Teardown**:
  - Deleted `peering-1-2`, which deactivated both connections
  - Verified internal ping no longer worked (100% packet loss)

---

## 🧩 Skills Applied

- VPC Network Design
- Internal IP Routing
- VPC Peering Configuration
- Firewall and Route Inspection
- Troubleshooting Network Connectivity

---

## 📁 Lab File Location

```
google_cloud_security_specialization/
└── 2-securing-gcp-infrastructure/
    └── vpc_peering_lab_summary.md
```

---

## 👩‍💻 Author

**Lisa Mary Lee**  
💼 [LinkedIn](https://www.linkedin.com/in/lisamarylee)  
📫 lisamarylee@gmail.com

---

## 📜 License

Licensed under the [MIT License](LICENSE).
