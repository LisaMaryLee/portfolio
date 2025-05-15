# 🛡️ Lab: Configuring Traffic Blocklisting with Google Cloud Armor

---

## 🧪 Lab Summary

This lab demonstrates how to blocklist traffic at the edge of Google's global network using **Google Cloud Armor**. You work with an Application Load Balancer (ALB), simulate client access, and block a specific IP address via a custom security policy. Cloud Armor enhances application security by enforcing policies close to the user.

---

## 🎯 Objectives

- Verify an existing **Application Load Balancer** with global backends
- Launch a test VM to access the load balancer
- Create a **Cloud Armor** policy to block traffic from a specific IP
- Apply the policy to the backend service of the load balancer
- Review Cloud Armor logs to confirm blocked requests

---

## 🧰 Reference Commands

```bash
# Check load balancer backend health
gcloud compute backend-services get-health web-backend --global

# Retrieve the load balancer IP address
gcloud compute forwarding-rules describe web-rule --global

# Create a test instance
gcloud compute instances create access-test --zone=ZONE

# Get external IP of test VM
gcloud compute instances list

# Create Cloud Armor security policy
gcloud compute security-policies create blocklist-access-test --description="Block access-test VM IP" --default-action=allow

# Add blocklist rule to the policy
gcloud compute security-policies rules create 1000   --security-policy=blocklist-access-test   --src-ip-ranges=ACCESS_TEST_VM_EXTERNAL_IP   --action=deny-404   --description="Block test VM"

# Attach security policy to backend service
gcloud compute backend-services update web-backend   --security-policy blocklist-access-test   --global

# View logs
gcloud logging read 'resource.type="http_load_balancer" AND resource.labels.backend_service_name="web-backend"' --limit=10
```

---

## 📊 Expected Results

- `access-test` VM is initially able to reach the load balancer via `curl`
- After applying the security policy, `curl` from the blocked IP returns `404 Not Found`
- Access from other IPs (e.g., browser) still succeeds
- Logs show Cloud Armor blocking traffic from the denied source IP

---

## 🧑‍💻 Author

**Lisa Mary Lee**  
💼 [LinkedIn](https://www.linkedin.com/in/lisamarylee)  
📫 lisamarylee@gmail.com

---

## 📜 License

Licensed under the [MIT License](LICENSE). You may adapt or reuse with attribution.
