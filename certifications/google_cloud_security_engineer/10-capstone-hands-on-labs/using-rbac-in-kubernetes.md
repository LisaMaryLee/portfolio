# Using Role-based Access Control in Kubernetes Engine
**Completed by:** Lisa Mary Lee
**Date:** May 15, 2025

## Lab Objectives
- Assign read-write and read-only permissions to user personas (owner, auditor)
- Grant limited Kubernetes API access to a running application
- Debug RBAC misconfigurations using pod logs and Kubernetes audit events

## Key Steps
### 1. Environment Setup
- Verified `rbac-demo-cluster` with Legacy Authorization disabled
- Used Terraform to create roles, namespaces, and test user VMs

### 2. Role-based Access Setup
- Owner: Full access to `dev`, `test`, and `prod` namespaces
- Auditor: Read-only access to the `dev` namespace only
- Confirmed access restrictions using `kubectl` from respective simulated user VMs

### 3. Application RBAC Scenario
- Deployed a `pod-labeler` application using a Kubernetes ServiceAccount
- Debugged `403 Forbidden` errors due to missing serviceAccount and insufficient RBAC `verbs`
- Applied 2 fixes:
  - Fix 1: Assigned correct `serviceAccountName`
  - Fix 2: Updated `Role` with `list` and `patch` permissions

### 4. Troubleshooting
- Used `kubectl logs` and `describe` to isolate permission errors
- Validated through GKE audit logs with `protoPayload.methodName="io.k8s.core.v1.pods.patch"`

## Final Verification
- Observed `updated` label applied to pods by `pod-labeler`
- No RBAC errors in logs

## Key Takeaways
- Always verify the ServiceAccount and associated RoleBindings
- Use logs, audit trails, and Kubernetes `describe` to debug RBAC failures
- GKE RBAC integrates with IAM roles for API access, and Kubernetes-native RoleBindings for in-cluster access
