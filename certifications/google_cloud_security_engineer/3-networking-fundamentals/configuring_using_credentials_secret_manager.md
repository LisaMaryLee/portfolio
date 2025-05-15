
# Configuring and Using Credentials with Secret Manager

This document summarizes the lab activities for securely managing credentials using **Secret Manager** on Google Cloud.

## Objectives
- Enable the Secret Manager API
- Create and manage secrets
- Access secret versions using CLI
- Rotate, disable, and re-enable secret versions

## Tasks Overview

### Task 1: Enable the Secret Manager API
- Enable the Secret Manager API via Google Cloud Console

### Task 2: Create a secret
- Secret name: `password`
- Secret value: `xyzpdq`
- Label: `team=acme`

### Task 3: Use the secret
- Access version 1 via `gcloud secrets versions access`
- Output confirms stored value `xyzpdq`

### Task 4: Create and use a new secret version
- Add version 2 with value `abc123`
- Access version 2 and `latest` using CLI
- Verify that latest points to `abc123`

### Task 5: Create a new version and disable prior versions
- Add version 3 with value `def123`
- Disable versions 1 and 2
- Access to version 2 now fails with `FAILED_PRECONDITION`

### Task 6: Reinstate and verify a previous version
- Re-enable version 2 via UI
- Verify CLI access to version 2 (`abc123`) is restored

## Conclusion
This lab demonstrated how to create, version, and control access to secrets using Secret Manager. You also learned how to manage lifecycle stages such as disabling and re-enabling previous versions securely via the Console and CLI.
