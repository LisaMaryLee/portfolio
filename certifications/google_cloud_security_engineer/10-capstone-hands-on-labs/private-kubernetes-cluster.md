# 🛡️ Setting up a Private Kubernetes Cluster (GSP178)

## Overview
In this lab, you created a **private GKE cluster** where:
- Nodes have **no external IPs**
- Master is **not accessible from the public internet**
- VPC peering is used for communication between master and nodes

---

## ✅ Tasks Completed

### 1. **Set Region and Zone**
```bash
gcloud config set compute/zone ZONE
export REGION=REGION
export ZONE=ZONE
```

---

### 2. **Create Private Cluster (Auto Subnet)**
```bash
gcloud beta container clusters create private-cluster \
    --enable-private-nodes \
    --master-ipv4-cidr 172.16.0.16/28 \
    --enable-ip-alias \
    --create-subnetwork ""
```

---

### 3. **View Subnet and Secondary Ranges**
```bash
gcloud compute networks subnets list --network default
gcloud compute networks subnets describe SUBNET_NAME --region=$REGION
```

---

### 4. **Enable Master Authorized Networks**
- Create VM:
```bash
gcloud compute instances create source-instance --zone=$ZONE --scopes cloud-platform
```

- Get external IP of VM:
```bash
gcloud compute instances describe source-instance --zone=$ZONE | grep natIP
```

- Authorize master access:
```bash
gcloud container clusters update private-cluster \
    --enable-master-authorized-networks \
    --master-authorized-networks <natIP>/32
```

- SSH into source-instance and install tools:
```bash
sudo apt-get install kubectl google-cloud-sdk-gke-gcloud-auth-plugin
gcloud container clusters get-credentials private-cluster --zone=$ZONE
```

- Verify node IPs:
```bash
kubectl get nodes --output wide
```

---

### 5. **Delete the Private Cluster**
```bash
gcloud container clusters delete private-cluster --zone=$ZONE
```

---

### 6. **Create Private Cluster with Custom Subnetwork**
```bash
gcloud compute networks subnets create my-subnet \
    --network default \
    --range 10.0.4.0/22 \
    --enable-private-ip-google-access \
    --region=$REGION \
    --secondary-range my-svc-range=10.0.32.0/20,my-pod-range=10.4.0.0/14

gcloud beta container clusters create private-cluster2 \
    --enable-private-nodes \
    --enable-ip-alias \
    --master-ipv4-cidr 172.16.0.32/28 \
    --subnetwork my-subnet \
    --services-secondary-range-name my-svc-range \
    --cluster-secondary-range-name my-pod-range \
    --zone=$ZONE
```

- Authorize external access again:
```bash
gcloud container clusters update private-cluster2 \
    --enable-master-authorized-networks \
    --zone=$ZONE \
    --master-authorized-networks <natIP>/32
```

- Connect and verify again:
```bash
gcloud compute ssh source-instance --zone=$ZONE
gcloud container clusters get-credentials private-cluster2 --zone=$ZONE
kubectl get nodes --output wide
```

---

## 🎉 Congratulations!
You successfully:
- Created two types of **private GKE clusters**
- Verified node isolation
- Controlled access to the Kubernetes master

---

## 🔗 Learn More
- [Private clusters overview](https://cloud.google.com/kubernetes-engine/docs/concepts/private-cluster-concept)
- [Authorized networks for master access](https://cloud.google.com/kubernetes-engine/docs/how-to/private-clusters#adding_authorized_networks)
