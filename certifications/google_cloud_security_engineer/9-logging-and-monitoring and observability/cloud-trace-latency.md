# View application latency with Cloud Trace

**Course:** Google Cloud Observability Labs  
**Module:** Cloud Trace Fundamentals  
**Completed by:** Lisa Mary Lee  
**Date:** May 15, 2025

---

## 🧠 Objectives

In this lab, you learned how to:

- Deploy a sample application to a Google Kubernetes Engine (GKE) cluster.
- Generate a trace by sending HTTP requests to the application.
- Use the Cloud Trace UI to inspect latency data and understand distributed spans.

---

## 🚀 Steps Completed

### 1. Deploy Sample App to GKE

- Cloned Google Cloud’s Python sample repo.
- Enabled GKE API.
- Created GKE cluster: `cloud-trace-demo`
- Updated kubeconfig and verified access.
- Deployed three microservices using `setup.sh`:  
  - `cloud-trace-demo-a`, `cloud-trace-demo-b`, `cloud-trace-demo-c`

### 2. Create and Observe a Trace

- Sent HTTP requests to service A using `curl $(kubectl get svc ...)`.
- Verified cascading output from services A → B → C.

### 3. Use Cloud Trace UI

- Accessed: **Navigation > Observability > Trace**
- Viewed heatmap of spans and detailed individual trace timelines.
- Clicked on darker spans to review slow responses and timing relationships.
- Analyzed nested span breakdown by service and component.

---

## 📊 Insights

- Cloud Trace heatmaps help isolate latency bottlenecks in distributed services.
- Individual spans provide method-level insights with duration and error data.
- Repeated `curl` calls showed request-response consistency across chained services.

---

## ✅ Outcome

Cloud Trace was successfully used to visualize and analyze application latency in a live Kubernetes cluster environment. This reinforced how distributed tracing helps developers diagnose and optimize microservices communication.

