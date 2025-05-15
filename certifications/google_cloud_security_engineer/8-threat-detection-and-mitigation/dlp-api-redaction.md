# Redacting Sensitive Data with the DLP API

**Lab Title:** Redacting Sensitive Data with the DLP API  
**Level:** Introductory  
**Duration:** 1 hour  
**Cost:** No cost  

---

## 🧠 Overview

Google Cloud's Data Loss Prevention (DLP) API helps classify and redact sensitive data such as email addresses, phone numbers, credit card numbers, and other PII. In this lab, you will use the Node.js DLP SDK to inspect strings and redact data from both strings and images.

---

## 🎯 Objectives

- Enable the DLP API
- Install Node.js and DLP client library with sample code
- Inspect string data for sensitive information
- Redact sensitive data from strings
- Redact sensitive data from images

---

## 🛠️ Setup

- Open an incognito window to log into Qwiklabs
- Click **Start Lab** and note the **Username** and **Password**
- Open **Google Cloud Console**
- Use only the credentials provided (do not use your own account)

---

## 🚀 Task 1: Enable the DLP API

1. Go to **Navigation menu > APIs & Services**
2. Click **Enable APIs and Services**
3. Search for **DLP**
4. Click on **Sensitive Data Protection (DLP)** and **Enable**

---

## 📥 Task 2: Install the DLP API and Node.js Samples

```bash
# Set environment variable
export GCLOUD_PROJECT=$DEVSHELL_PROJECT_ID

# Clone sample code repo
git clone https://github.com/GoogleCloudPlatform/nodejs-docs-samples

# Navigate to DLP samples
cd nodejs-docs-samples/dlp

# Install dependencies
npm install @google-cloud/dlp
npm install yargs
npm install mime@2.5.2
```

---

## 🔍 Task 3: Inspect and Redact Sensitive Data

### Inspect a String

```bash
node inspectString.js $GCLOUD_PROJECT "My email address is joe@example.com."
node inspectString.js $GCLOUD_PROJECT "My phone number is 555-555-5555."
```

### Mask a String

```bash
node deidentifyWithMask.js $GCLOUD_PROJECT "My phone number is 555-555-5555."
```

### Redact an Image

1. Save the sample image as `dlp-input.png`
2. Upload it to Cloud Shell
3. Run:

```bash
node redactImage.js $GCLOUD_PROJECT ~/dlp-input.png "" EMAIL_ADDRESS ~/dlp-redacted.png
```

4. Use **Open Editor** to verify the redacted image

---

## ✅ Completion

You successfully:

- Enabled and used the DLP API
- Inspected and redacted string content
- Redacted email address in image using DLP

---

## 📚 Further Reading

- [DLP Documentation](https://cloud.google.com/dlp/docs)
- [Node.js SDK Samples](https://github.com/GoogleCloudPlatform/nodejs-docs-samples/tree/main/dlp)

