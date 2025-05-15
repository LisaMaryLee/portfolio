# Identify Application Vulnerabilities with Security Command Center

## Overview
This lab demonstrates how to identify and remediate a Cross-Site Scripting (XSS) vulnerability in a Python Flask application using **Google Cloud Security Command Center's Web Security Scanner (WSS)**.

---

## Objectives
- Deploy a vulnerable application on a Compute Engine instance.
- Use **Web Security Scanner** to detect security vulnerabilities.
- Fix the XSS vulnerability in the application.
- Re-scan and verify the issue is resolved.

---

## Key Steps and Commands

### Step 1: Launch a VM and Create Firewall Rule
```bash
gcloud compute addresses create xss-test-ip-address --region=REGION
gcloud compute addresses describe xss-test-ip-address --region=REGION --format="value(address)"

gcloud compute instances create xss-test-vm-instance   --address=xss-test-ip-address --no-service-account   --no-scopes --machine-type=e2-micro --zone=ZONE   --metadata=startup-script='apt-get update; apt-get install -y python3-flask'

gcloud compute firewall-rules create enable-wss-scan   --direction=INGRESS --priority=1000 --network=default   --action=ALLOW --rules=tcp:8080 --source-ranges=0.0.0.0/0
```

### Step 2: Deploy Vulnerable Flask App
```bash
gsutil cp gs://cloud-training/GCPSEC-ScannerAppEngine/flask_code.tar .
tar xvf flask_code.tar
python3 app.py
```

- Access app at: `http://<EXTERNAL_IP>:8080`
- Test XSS: `<script>alert('This is an XSS Injection')</script>`

---

### Step 3: Enable Web Security Scanner API
- Enable from API Library:
  - `Web Security Scanner API`

---

### Step 4: Run Initial Scan
- Go to **Security > Web Security Scanner > + New Scan**
- Set URL to `http://<EXTERNAL_IP>:8080`
- Save and click **Run**
- XSS vulnerability will be detected in results.

---

### Step 5: Fix XSS in `app.py`
```python
# Replace:
# output_string = input_string
# With:
output_string = "".join([html_escape_table.get(c, c) for c in input_string])
```
- Restart app:
```bash
python3 app.py
```
- Test input again in browser — output should appear as raw text.

---

### Step 6: Re-run Scan
- Return to **Web Security Scanner**
- Click **Run** again
- Confirm **no vulnerabilities detected**

---

## Summary
Web Security Scanner on GCP can:
- Detect XSS and other vulnerabilities
- Automate testing across applications
- Verify remediation by re-running scans

This lab demonstrates secure DevOps workflows for detecting and resolving app vulnerabilities early in the cloud development lifecycle.