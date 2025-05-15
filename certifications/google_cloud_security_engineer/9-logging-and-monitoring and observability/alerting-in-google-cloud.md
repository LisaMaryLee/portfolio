# Alerting in Google Cloud

## Overview
This lab walks you through deploying an App Engine application and setting up various alerting policies using Google Cloud Monitoring and Alerting.

## Objectives
- Deploy an application to App Engine
- Create latency and error rate alerting policies
- Use Cloud Monitoring and Alerting to manage incidents
- (Optional) Configure alerting policies via CLI

## Key Commands and Steps
### Deploy App Engine App
```bash
git clone --depth 1 https://github.com/GoogleCloudPlatform/training-data-analyst.git
cd ~/training-data-analyst/courses/design-process/deploying-apps-to-gcp
pip3 install -r requirements.txt
python3 main.py
gcloud app create --region=REGION
gcloud app deploy --version=one --quiet
```

### Create App Engine Latency Alert
- Metric: `GAE Application > Http > Response latency`
- Aggregator: 99th percentile
- Threshold: 8000ms over 1 minute
- Action: Email notification

### Generate Alert
- Modify app to include `time.sleep(10)`
- Redeploy and simulate traffic with:
```bash
while true; do curl -s https://$DEVSHELL_PROJECT_ID.appspot.com/ | grep -e "<title>" -e "error";sleep .$[( $RANDOM % 10 )]s;done
```

### Optional: Create Alert with CLI
- Create policy file: `app-engine-error-percent-policy.json`
- Deploy policy:
```bash
gcloud alpha monitoring policies create --policy-from-file="app-engine-error-percent-policy.json"
```
- Trigger with 2% random error rate in app

## Cleanup
- Stop load generation
- Delete alerting policies
- Unsubscribe notification channels

## Conclusion
You successfully configured Google Cloud alerting policies for an App Engine app, both via console and CLI.

