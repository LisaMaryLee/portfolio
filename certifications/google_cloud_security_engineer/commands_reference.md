
# 📘 Google Cloud Security Engineer Certification  
**Command Reference Guide – Labs Summary**  
_Last updated: May 15, 2025_

---
## **2. Core Infrastructure Review**
```bash
gcloud config set project PROJECT_ID
gcloud config set compute/zone ZONE
gcloud config set compute/region REGION
```

---

## **3. Networking Fundamentals**
```bash
gcloud compute networks create custom-network --subnet-mode=custom
gcloud compute networks subnets create subnet-1 \
  --network=custom-network --region=REGION --range=10.0.0.0/24
gcloud compute firewall-rules create allow-ssh --allow=tcp:22
gcloud compute instances create vm-instance \
  --zone=ZONE --network=custom-network --subnet=subnet-1
```

---

## **4. Routing and Architecture**
```bash
gcloud compute routes create custom-route \
  --network=custom-network --destination-range=0.0.0.0/0 \
  --next-hop-gateway=default-internet-gateway
gcloud compute instances add-access-config INSTANCE_NAME
```

---

## **5. Network Security and Balancing**
```bash
gcloud compute firewall-rules create allow-health-checks --network=default \
  --allow tcp --source-ranges 130.211.0.0/22,35.191.0.0/16
gcloud compute forwarding-rules list
gcloud compute target-pools create www-pool --region=REGION
```

---

## **6. Hybrid and Multicloud**
```bash
gcloud compute vpn-gateways create vpn-gateway-1 --network=default --region=REGION
gcloud compute interconnects describe INTERCONNECT_NAME
```

---

## **7. Access and Policy Management**
```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="user:EMAIL" \
  --role="roles/viewer"

gcloud iam roles create customRoleId \
  --project=PROJECT_ID \
  --file=role-definition.yaml

gcloud iam roles update customRoleId \
  --project=PROJECT_ID \
  --add-permissions="storage.buckets.get"
```

---

## **8. Threat Detection and Mitigation**
```bash
gcloud services enable securitycenter.googleapis.com
gcloud scc sources list --organization=ORG_ID
gcloud scc findings list --source=SOURCE_ID --organization=ORG_ID
```

---

## **9. Logging and Monitoring and Observability**
```bash
gcloud logging read "resource.type=gce_instance"
gcloud logging logs list
gcloud monitoring policies list
gcloud monitoring channels list
```

---

## **10. Capstone Hands-on Labs**
```bash
kubectl create namespace secure-app
kubectl apply -f secure-deployment.yaml
kubectl auth can-i get pods --as=system:serviceaccount:default:pod-labeler
```

---

## ✅ Common Across All Labs
```bash
gcloud auth list
gcloud config list project
gcloud container clusters get-credentials CLUSTER_NAME --zone=ZONE
kubectl get pods
kubectl logs POD_NAME
kubectl apply -f FILE.yaml
```
