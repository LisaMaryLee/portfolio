# 🌐 Lab: Cloud DNS - Traffic Steering using Geolocation Policy

## 🧪 Lab Summary

This lab focuses on configuring and testing **Cloud DNS Geolocation routing policies**. You’ll route client requests to the nearest region’s web server using DNS responses based on geographic source IPs.

---

## 🎯 Objectives

- Enable Compute and DNS APIs
- Launch client VMs in three regions (US, Europe, Asia)
- Launch web servers in US and Europe only
- Create a private DNS zone with geolocation routing
- Use cURL to test region-based resolution from clients
- Demonstrate fallback behavior when no exact region match exists
