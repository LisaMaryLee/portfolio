# 🧪 Lab Summary: Analyzing Network Traffic with VPC Flow Logs
**Completed on:** May 15, 2025

## ✅ Lab Objectives
- Configure a custom network with VPC flow logs.
- Create an Apache web server.
- Verify that network traffic is logged.
- Export the network traffic to BigQuery to analyze the logs.
- Set up VPC Flow Log aggregation settings.

## 🛠️ Tasks Completed

### Task 1: Configure a Custom Network with VPC Flow Logs
- Created a custom-mode VPC network (`vpc-net`) and subnet (`vpc-subnet`) with IP range `10.1.3.0/24`.
- Enabled VPC Flow Logs for the subnet.
- Created firewall rule (`allow-http-ssh`) to allow TCP ports 80 (HTTP) and 22 (SSH).

### Task 2: Create an Apache Web Server
- Created Compute Engine VM instance `web-server` on the custom VPC.
- Installed Apache2 and deployed a custom index page displaying `Hello World!`.

### Task 3: Verify Network Traffic is Logged
- Accessed the web server externally to generate HTTP traffic.
- Located log entries in Logs Explorer for subnetwork and flow logs.
- Filtered logs to include only entries from the source IP.
- Verified log fields: source/destination IPs, ports, and protocol.

### Task 4: Export Network Traffic to BigQuery for Analysis
- Created a log sink named `bq_vpcflows` exporting flow logs to BigQuery dataset.
- Accessed the web server repeatedly via curl to generate traffic.
- Queried BigQuery for:
  - Top IPs interacting with the server.
  - Most traffic exchanged by port and protocol.

### Task 5: Add VPC Flow Log Aggregation
- Modified `vpc-subnet` to use:
  - Aggregation interval of 30 seconds.
  - Sampling rate of 25%.
- Observed the expected reduction in daily log volume.


## 🎉 Conclusion

You configured VPC Flow Logs on a custom network, deployed a web server, verified and exported flow logs to BigQuery, then analyzed the logs using SQL queries. Finally, you configured aggregation settings to optimize storage and visibility.

