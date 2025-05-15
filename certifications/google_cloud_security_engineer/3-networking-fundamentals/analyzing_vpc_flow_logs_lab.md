# 🌐 Lab: Analyzing Network Traffic with VPC Flow Logs

---

## 🧪 Lab Summary

This lab walks through the process of enabling and analyzing **VPC Flow Logs** in Google Cloud. You'll configure a custom network, launch an Apache web server, and monitor network traffic using Cloud Logging and BigQuery.

---

## 🎯 Objectives

- Configure a custom VPC network with VPC Flow Logs enabled
- Deploy an Apache web server to generate traffic
- Verify traffic is logged via Cloud Logging
- Export flow logs to BigQuery and analyze traffic patterns
- Enable log sampling and aggregation to reduce log volume and cost

---

## 📦 Artifacts Created

- VPC network `vpc-net` and subnetwork `vpc-subnet`
- Firewall rule `allow-http-ssh`
- Compute Engine instance `web-server` with Apache installed
- Log sink to BigQuery dataset `bq_vpcflows`
- Sampled BigQuery queries for flow log analysis
- VPC Flow Logs aggregation settings: 30s interval, 25% sample rate

---

## 🧠 Key Concepts

- VPC Flow Logs provide visibility into network traffic for VMs
- Logs can be filtered and analyzed in Cloud Logging or exported to BigQuery
- Aggregation and sampling settings reduce log volume and cost while preserving insights

---

## 🧑‍💻 Author

**Lisa Mary Lee**  
💼 [LinkedIn](https://www.linkedin.com/in/lisamarylee)  
📫 lisamarylee@gmail.com

---

## 📜 License

Licensed under the [MIT License](LICENSE). You may adapt or reuse templates with attribution.
