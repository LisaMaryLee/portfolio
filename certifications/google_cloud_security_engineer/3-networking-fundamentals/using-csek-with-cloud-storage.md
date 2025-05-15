
# Using Customer-Supplied Encryption Keys with Cloud Storage

## Overview
Cloud Storage encrypts your data server-side with a Google-managed encryption key by default. This lab demonstrates how to configure customer-supplied encryption keys (CSEK) for greater control over encryption.

## Objectives
- Configure CSEK for Cloud Storage.
- Upload encrypted files to Cloud Storage.
- Verify encryption and file retrieval.
- Rotate CSEK keys without downloading/re-uploading data.

---

## Task 1: Configure Required Resources

### Step 1: Create a Service Account
```bash
gcloud iam service-accounts create cseklab --display-name "CSEK Lab Service Account"
```

### Step 2: Create a Compute Engine VM
- Name: `cseklab-vm`
- Series: `E2`
- Machine type: `e2-micro`
- Service account: `cseklab`
- Access scopes: `Set access for each API`, Storage: `Full`

### Step 3: Create a Cloud Storage Bucket
```bash
export BUCKET_NAME=$(gcloud config get-value project)-csek
gsutil mb -l us gs://$BUCKET_NAME
```

### Step 4: Download Sample File and Make Copies
```bash
curl https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/ClusterSetup.html > setup.html
cp setup.html setup2.html
cp setup.html setup3.html
```

---

## Task 2: Configure Customer-Supplied Encryption Keys

### Step 1: Generate Encryption Key
```bash
openssl rand 32 > mykey.txt
openssl base64 -in mykey.txt
```

### Step 2: Update .boto Configuration
```bash
gsutil config -n
nano .boto
# Add or uncomment:
encryption_key=<base64-key>
```

### Step 3: Upload Encrypted Files
```bash
gsutil cp setup.html gs://$BUCKET_NAME
gsutil cp setup2.html gs://$BUCKET_NAME
```

### Step 4: Retrieve File to Verify Decryption
```bash
rm setup.html
gsutil cp gs://$BUCKET_NAME/setup.html ./
cat setup.html
```

---

## Task 3: Rotate CSEK Keys

### Step 1: Generate New Key
```bash
openssl rand 32 > mykey.txt
openssl base64 -in mykey.txt
```

### Step 2: Update .boto with New Key
```bash
# Comment previous encryption_key
# Add:
encryption_key=<new-base64-key>
decryption_key1=<old-base64-key>
```

### Step 3: Upload New File and Verify Old Files
```bash
gsutil cp setup3.html gs://$BUCKET_NAME
rm setup2.html setup3.html
gsutil cp gs://$BUCKET_NAME/setup2.html ./
gsutil cp gs://$BUCKET_NAME/setup3.html ./
```

### Step 4: Rotate Encryption Key on Existing Object
```bash
gsutil rewrite -k gs://$BUCKET_NAME/setup.html
```

### Step 5: Final Verification
```bash
rm setup*.html
gsutil cp gs://$BUCKET_NAME/setup.html ./
gsutil cp gs://$BUCKET_NAME/setup3.html ./
cat setup.html
cat setup3.html

# This will fail:
gsutil cp gs://$BUCKET_NAME/setup2.html ./
```

---

## Completion
You have successfully:
- Configured and tested CSEK encryption.
- Rotated encryption keys.
- Verified encryption behavior through decryption and file access.

