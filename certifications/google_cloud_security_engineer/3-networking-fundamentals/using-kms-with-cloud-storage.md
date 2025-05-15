# Using Customer-Managed Encryption Keys with Cloud Storage and Cloud KMS

## Overview
This lab demonstrated how to manage and use Cloud Key Management Service (Cloud KMS) to encrypt data stored in Cloud Storage using customer-managed encryption keys (CMEK).

---

## Objectives
- Create and manage KMS KeyRings and CryptoKeys.
- Set a default encryption key for Cloud Storage buckets.
- Encrypt objects using Cloud KMS keys.
- Perform key rotation and manual server-side encryption using REST API.
- Use IAM for key permissions and audit Cloud KMS usage.

---

## Tasks

### Task 1: Configure Required Resources
- Created a Cloud Storage bucket with a globally unique name.
- Created sample files and uploaded one (`file1.txt`) using Google-managed keys.
- Enabled the `cloudkms.googleapis.com` API.

### Task 2: Use Cloud KMS
- Created a KeyRing (`lab-keyring`) and two CryptoKeys (`labkey-1` and `labkey-2`) in a specific region.
- Verified the creation in the Security > Key Management section of the Console.

### Task 3: Add a Default Key for a Bucket
- Granted permissions for the storage service account to use both KMS keys.
- Set `labkey-1` as the default encryption key for the bucket.
- Uploaded `file2.txt`, which was encrypted with `labkey-1`.

### Task 4: Encrypt Individual Objects
- Used `labkey-2` to encrypt `file3.txt` without changing the default key.
- Verified file encryption types via the console and `gsutil ls -L`.

### Task 5: Perform Key Rotation
- Enabled automatic rotation (30 days) for `labkey-1`.
- Manually rotated `labkey-2`, creating a new version.
- Reviewed, but did not destroy, key versions.

### Bonus Task: Encrypt/Decrypt via REST API
- Encoded plaintext using base64 and encrypted with REST API.
- Decrypted ciphertext and verified integrity using `curl`, `jq`, and `base64`.

---

## Key Commands Used
```bash
# Create KeyRing and CryptoKeys
gcloud kms keyrings create lab-keyring --location=Region
gcloud kms keys create labkey-1 --location=Region --keyring=lab-keyring --purpose=encryption
gcloud kms keys create labkey-2 --location=Region --keyring=lab-keyring --purpose=encryption

# Set default key
gsutil kms encryption -k projects/$DEVSHELL_PROJECT_ID/locations/Region/keyRings/lab-keyring/cryptoKeys/labkey-1 gs://$DEVSHELL_PROJECT_ID-kms

# Upload and encrypt file with non-default key
gsutil -o "GSUtil:encryption_key=..." cp file3.txt gs://$DEVSHELL_PROJECT_ID-kms

# Manual encryption/decryption via REST
curl ...:encrypt ...
curl ...:decrypt ...
```

---

## Outcome
- Successfully used Cloud KMS to manage customer-managed encryption.
- Demonstrated key rotation and encryption policy enforcement.
- Practiced encryption operations using both CLI and REST API.

