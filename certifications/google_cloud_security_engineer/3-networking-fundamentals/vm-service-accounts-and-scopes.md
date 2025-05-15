# Configuring, Using, and Auditing VM Service Accounts and Scopes

## Overview
This lab focuses on configuring and using service accounts for VM instances in Google Cloud. You will create service accounts, associate them with Compute Engine instances, and use them to securely access BigQuery public datasets.

## Objectives
- Create and manage service accounts
- Create a virtual machine and associate it with a service account
- Use client libraries to access BigQuery from a service account
- Run a query on a BigQuery public dataset from a Compute Engine instance

## Task 1: Create and Manage Service Accounts

### Step 1: Create a service account
```bash
gcloud iam service-accounts create my-sa-123 --display-name "my service account"
```

### Step 2: Grant project-level IAM roles to the service account
```bash
gcloud projects add-iam-policy-binding $DEVSHELL_PROJECT_ID \
    --member serviceAccount:my-sa-123@$DEVSHELL_PROJECT_ID.iam.gserviceaccount.com --role roles/editor
```

## Task 2: Use the Client Libraries to Access BigQuery

### Step 1: Create a new service account for BigQuery access
In the Console UI:
- Create service account: `bigquery-qwiklab`
- Roles: BigQuery Data Viewer, BigQuery User

### Step 2: Create a VM with service account attached
- Name: `bigquery-instance`
- Series: E2, Machine type: `e2-standard-2`
- Boot disk: Debian GNU/Linux 11
- Enable Shielded VM, turn on Secure Boot
- Service account: `bigquery-qwiklab`
- Access Scopes: Allow full access to all Cloud APIs

### Step 3: SSH into the instance and install dependencies
```bash
sudo apt-get update -y
sudo apt-get install -y git python3-pip
sudo pip3 install six==1.13.0
sudo pip3 install --upgrade pip google-cloud-bigquery pandas pyarrow==16.1.0 db-dtypes
```

### Step 4: Create Python script for BigQuery access
```bash
echo "
from google.auth import compute_engine
from google.cloud import bigquery

credentials = compute_engine.Credentials(
    service_account_email='YOUR_SERVICE_ACCOUNT')

query = '''
SELECT
  year,
  COUNT(1) as num_babies
FROM
  publicdata.samples.natality
WHERE
  year > 2000
GROUP BY
  year
'''

client = bigquery.Client(
    project='YOUR_PROJECT_ID',
    credentials=credentials)
print(client.query(query).to_dataframe())
" > query.py
```

### Step 5: Replace placeholders in script
```bash
sed -i -e "s/YOUR_PROJECT_ID/$(gcloud config get-value project)/g" query.py
sed -i -e "s/YOUR_SERVICE_ACCOUNT/bigquery-qwiklab@$(gcloud config get-value project).iam.gserviceaccount.com/g" query.py
```

### Step 6: Run the query
```bash
python3 query.py
```

## Summary
You created and configured a service account, attached it to a VM, and securely accessed BigQuery public datasets using client libraries from that VM.

