# Using Network Policy on Google Kubernetes Engine

## Overview
This guide demonstrates how to secure Kubernetes Engine by enforcing fine-grained network communication restrictions using Network Policies.

## Key Concepts
- **Network Policies**: Control communication between pods using labels and namespaces.
- **Dataplane V2**: Enables network policies by default in GKE.
- **Bastion Host**: Used to securely access a private GKE cluster.

## Lab Architecture
- Private GKE cluster (no public endpoint)
- Bastion host with firewall rules allowing SSH
- Three workloads:
  - `hello-server`: HTTP service
  - `hello-client-allowed`: Can access `hello-server`
  - `hello-client-blocked`: Should be blocked by network policy

## Steps
1. **Setup:**
   - Enable required APIs
   - Clone lab resources
   - Configure Terraform variables

2. **Provision Infrastructure:**
   - Run `make tf-apply`
   - SSH into bastion
   - Configure `kubectl` authentication

3. **Deploy Workloads:**
   - Apply manifests in `./manifests/hello-app/`
   - Validate all clients can reach `hello-server`

4. **Apply Network Policy:**
   - Apply `./manifests/network-policy.yaml`
   - Verify only labeled pods can connect

5. **Namespace Isolation:**
   - Deploy namespace-based policy from `network-policy-namespaced.yaml`
   - Move allowed clients into new namespace `hello-apps`

## Cleanup
- Run `make teardown` after logging out of bastion host.

## Learn More
- [Kubernetes Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
- [Terraform Google Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
