# 🚀 Hello Cloud Run

This lab demonstrates deploying a simple containerized Node.js app using Cloud Run, a fully managed serverless platform on Google Cloud.

---

## 🎯 Objectives

- Enable the Cloud Run API  
- Build and containerize a Node.js app  
- Upload the image to Artifact Registry  
- Deploy to Cloud Run  
- Clean up resources

---

## 🧰 Tools Used

- Google Cloud Shell  
- gcloud CLI  
- Docker  
- Cloud Build  
- Cloud Run  

---

## 📝 Steps

### 1. Enable the Cloud Run API and Set Environment

```bash
gcloud services enable run.googleapis.com
gcloud config set compute/region "REGION"
export LOCATION="REGION"
```

### 2. Create the Node.js App

```bash
mkdir helloworld && cd helloworld

nano package.json
# Add:
# {
#   "name": "helloworld",
#   ...
# }

nano index.js
# Add:
# const express = require('express');
# ...
```

### 3. Create Dockerfile and Build Container

```bash
nano Dockerfile
# Add Docker instructions

gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/helloworld
gcloud container images list
gcloud auth configure-docker
```

Test it locally:
```bash
docker run -d -p 8080:8080 gcr.io/$GOOGLE_CLOUD_PROJECT/helloworld
```

Use Web Preview on port 8080.

---

### 4. Deploy to Cloud Run

```bash
gcloud run deploy --image gcr.io/$GOOGLE_CLOUD_PROJECT/helloworld --allow-unauthenticated --region=$LOCATION
```

✅ You will receive a service URL like:
```
https://helloworld-xxxxx.a.run.app
```

---

### 5. Cleanup

```bash
gcloud container images delete gcr.io/$GOOGLE_CLOUD_PROJECT/helloworld
gcloud run services delete helloworld --region="REGION"
```

---

## 🧪 Result

Deployed and tested a scalable, stateless container application using Cloud Run. Great for modern cloud-native web services.

