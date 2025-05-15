# 🔐 Lab: Implement Private Google Access and Cloud NAT

**Course:** Preparing for Google Cloud Certification: Cloud Security Engineer  
**Module:** Network Services and Secure Connectivity  
**Completed by:** Lisa Mary Lee  
**Date:** May 15, 2025

---

## 🧪 Lab Summary

In this lab, you configured Private Google Access and Cloud NAT to enable internet and API access for a VM instance without an external IP address. This is a secure architecture pattern that supports patching and Google service access while avoiding public exposure.

---

## 🎯 Objectives

- Create a VM instance without an external IP address
- Enable Private Google Access at the subnet level
- Configure a NAT gateway using Cloud Router
- Validate access to Google APIs and public internet resources
- Enable and review NAT gateway logging in Cloud Logging

---

## 📁 Folder Structure

```
cloud_nat_and_private_google_access/
├── 1-vpc-network-setup/                   # Create VPC, subnet, and firewall rules
├── 2-vm-internal-no-external-ip/         # Instance without public IP
├── 3-enable-private-google-access/       # Access Google APIs via internal routing
├── 4-cloud-nat-configuration/            # NAT gateway for public internet access
├── 5-nat-logging-and-verification/       # Enable logging and view logs
└── README.md                             # Lab summary and commands
```

---

## 🧰 Reference Commands

```bash
# Create VPC and Subnet
gcloud compute networks create privatenet --subnet-mode=custom
gcloud compute networks subnets create privatenet-us   --network=privatenet --region=us-central1 --range=10.130.0.0/20

# Firewall Rule for IAP SSH Access
gcloud compute firewall-rules create privatenet-allow-ssh   --network=privatenet --allow=tcp:22,icmp --source-ranges=35.235.240.0/20

# VM Creation without External IP
gcloud compute instances create vm-internal   --zone=us-central1-a --machine-type=e2-medium --subnet=privatenet-us   --no-address

# Enable Private Google Access
gcloud compute networks subnets update privatenet-us   --region=us-central1 --enable-private-ip-google-access

# Cloud NAT Gateway
gcloud compute routers create nat-router   --network=privatenet --region=us-central1
gcloud compute routers nats create nat-config   --router=nat-router --region=us-central1 --auto-allocate-nat-external-ips   --nat-all-subnet-ip-ranges

# Enable NAT Logging
gcloud compute routers nats update nat-config   --router=nat-router --region=us-central1   --enable-logging --log-filter=ALL

# Access validation
gcloud compute ssh vm-internal --zone=us-central1-a --tunnel-through-iap
sudo apt-get update
gcloud storage cp gs://$MY_BUCKET/*.svg .
```

---

## ✅ Skills Demonstrated

- Cloud NAT configuration
- Private Google Access
- Identity-Aware Proxy tunneling
- Subnet-level API access control
- Cloud Logging for NAT audit trails

---

## 🧑‍💻 Author

**Lisa Mary Lee**  
💼 [LinkedIn](https://www.linkedin.com/in/lisamarylee)  
📫 lisamarylee@gmail.com

---

## 📜 License

Licensed under the [MIT License](LICENSE). You may reuse or adapt this lab documentation with proper attribution.
