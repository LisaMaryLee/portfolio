# Configuring and Using VPC Flow Logs in Cloud Logging

**Course:** Networking in Google Cloud  

---

## 🧠 Objectives

- Enable VPC flow logging for a subnet.
- Access logs via Cloud Logging.
- Filter logs for specific subnets, VMs, ports, or protocols.
- Perform network monitoring, forensics, and real-time security analysis.
- Disable VPC flow logging.

---

## ✅ Tasks and Key Actions

### Task 1: Enable VPC Flow Logging
- Enabled logging on subnets in Region1 and Region2 with `--enable-flow-logs` and `--logging-metadata=include-all`.
- Created test instances in three zones.

### Task 2: Generate Network Traffic
- Ran `ping`, `curl`, and `host` from `default-us-vm`, `default-eu-vm`, and `default-ap-vm`.
- Simulated DNS, HTTP, and ICMP traffic across regions.

### Task 3: View Logs in Cloud Logging
- Used **Logs Explorer** to view entries from `compute.googleapis.com/vpc_flows`.
- Inspected `jsonPayload.connection` fields for src/dest IP, port, protocol.

### Task 4: Advanced Filtering
- Used filters for:
  - Specific `src_ip` and `dest_ip`
  - Destination ports (22, 80, 53)
  - Protocols (UDP 17, TCP 6)
- Demonstrated logging only TCP and UDP (not ICMP).

### Task 5: Security Analysis
- Monitored for unwanted RDP attempts (port 3389).
- Validated how improperly scoped firewall rules can expose VM surfaces.

### Task 6: Log Exports and BigQuery Analysis
- Exported logs to BigQuery dataset `flowlogs_dataset`.
- Queried logs using SQL:
  ```sql
  SELECT jsonPayload.connection.dest_ip, resource
  FROM `flowlogs_dataset.compute_googleapis_com_vpc_flows*`
  WHERE jsonPayload.connection.dest_port = 22
  LIMIT 1000
  ```
- Exported logs to Cloud Pub/Sub for integration with SIEM systems.

### Task 7: Disable VPC Flow Logs
- Disabled logging using:
  ```bash
  gcloud compute networks subnets update default --region Region2 --no-enable-flow-logs
  ```

---

## 🔍 Review Summary

- **Flow logs** are crucial for **security monitoring**, **forensics**, and **troubleshooting**.
- Exporting to BigQuery and Pub/Sub allows **advanced analysis** and **stream processing**.
- ICMP traffic is **not** captured by VPC flow logs as of this lab.

---

