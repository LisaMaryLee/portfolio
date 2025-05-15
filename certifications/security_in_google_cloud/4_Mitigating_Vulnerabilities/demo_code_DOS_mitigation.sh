#!/bin/bash
gcloud compute firewall-rules create allow-internal     --direction=INGRESS     --priority=1000     --network=default     --action=ALLOW     --rules=tcp:22,tcp:80     --source-ranges=10.0.0.0/8
