# Securing Compute Engine Applications with BeyondCorp Enterprise

This document summarizes the lab activities for securing Compute Engine applications using Identity-Aware Proxy (IAP) from BeyondCorp Enterprise.

## Objectives
- Configure OAuth Consent
- Set up OAuth access credentials
- Set up IAP access
- Use IAP to restrict access

## Tasks Overview
### Task 1: Create a Compute Engine template
- Set up VM with startup script deploying Flask app

### Task 2: Create a managed instance group
- Based on instance template with 3 instances

### Task 3: Create a self-managed SSL certificate
- Use OpenSSL to create private key and CSR
- Create a self-signed certificate and a GCP SSL cert resource

### Task 4: Create a global external HTTPS Load Balancer
- Add backend service
- Attach managed instance group
- Configure frontend with self-signed SSL cert

### Task 5: Restart VMs
- Restart all 3 instances in the group to pick up updated configs

### Task 6: Configure Identity-Aware Proxy (IAP)
- Set OAuth consent screen and credentials
- Create firewall rule to allow only IAP traffic
- Enable IAP on backend service
- Grant IAP-secured Web App User role

### Task 7: Verify IAP protection
- Use `curl` to access LB IP and verify 302 redirect to accounts.google.com

## Conclusion
Successfully configured IAP to secure a web application running on Compute Engine. Access is now gated through identity verification.
