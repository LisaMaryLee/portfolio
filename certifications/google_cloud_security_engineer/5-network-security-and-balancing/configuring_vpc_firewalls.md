# 🔥 Lab: Configuring VPC Firewalls

---

## 🧪 Lab Summary

In this lab, you explored **Virtual Private Cloud (VPC)** network firewall rules in Google Cloud. You created auto and custom-mode networks, verified the behavior of the default network rules, and then built your own custom firewall rules to enable and restrict SSH, ICMP, and egress traffic using tags and rule priorities.

---

## 🎯 Objectives

- Create auto-mode and custom-mode VPC networks
- Investigate default and custom firewall rule behaviors
- Verify SSH/ICMP connectivity with firewall rules
- Apply target tags to enforce rule scope
- Use rule priorities to override allow/deny conditions
- Implement both ingress and egress rule scenarios

---

## 📌 Reference Commands

```bash
# Create auto-mode network
gcloud compute networks create mynetwork --subnet-mode=auto

# Create custom-mode network and subnet
gcloud compute networks create privatenet --subnet-mode=custom
gcloud compute networks subnets create privatesubnet \
  --network=privatenet --region=REGION --range=10.0.0.0/24 --enable-private-ip-google-access

# Create VM instances in various networks
gcloud compute instances create default-vm-1 --machine-type=e2-micro --zone=ZONE --network=default
gcloud compute instances create mynet-vm-1 --machine-type=e2-micro --zone=ZONE --network=mynetwork
gcloud compute instances create mynet-vm-2 --machine-type=e2-micro --zone=ZONE --network=mynetwork
gcloud compute instances create privatenet-bastion --machine-type=e2-micro --zone=ZONE --subnet=privatesubnet --can-ip-forward
gcloud compute instances create privatenet-vm-1 --machine-type=e2-micro --zone=ZONE --subnet=privatesubnet

# SSH into VM
gcloud compute ssh mynet-vm-2 --zone=ZONE

# Create custom ingress firewall rule with tag
gcloud compute firewall-rules create mynetwork-ingress-allow-ssh-from-cs \
  --network=mynetwork --action=ALLOW --direction=INGRESS --rules=tcp:22 \
  --source-ranges=$(curl -s https://api.ipify.org) --target-tags=lab-ssh

# Add tags to instances
gcloud compute instances add-tags mynet-vm-2 --zone=ZONE --tags=lab-ssh
gcloud compute instances add-tags mynet-vm-1 --zone=ZONE --tags=lab-ssh

# Create ICMP allow rule
gcloud compute firewall-rules create mynetwork-ingress-allow-icmp-internal \
  --network=mynetwork --action=ALLOW --direction=INGRESS --rules=icmp --source-ranges=10.128.0.0/9

# Create ICMP deny rule with higher priority (lower number)
gcloud compute firewall-rules create mynetwork-ingress-deny-icmp-all \
  --network=mynetwork --action=DENY --direction=INGRESS --rules=icmp --priority=500

# Update firewall rule priority
gcloud compute firewall-rules update mynetwork-ingress-deny-icmp-all --priority=2000

# Create egress deny rule
gcloud compute firewall-rules create mynetwork-egress-deny-icmp-all \
  --network=mynetwork --action=DENY --direction=EGRESS --rules=icmp --priority=10000
```

---

**Course:** Security in Google Cloud Specialization  
**Module:** Module 3  
**Completed by:** Lisa Mary Lee  
**Date:** May 15, 2025  
