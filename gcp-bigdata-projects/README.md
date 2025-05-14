# ☁️ GCP Big Data Projects

[![BigQuery](https://img.shields.io/badge/GCP-BigQuery-blue)](https://cloud.google.com/bigquery) 
[![Dataflow](https://img.shields.io/badge/GCP-Dataflow-brightgreen)](https://cloud.google.com/dataflow) 
[![Python](https://img.shields.io/badge/Python-3.7%2B-green.svg)](https://www.python.org/) 
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A collection of hands-on, real-world samples demonstrating Google Cloud Platform (GCP) Big Data workflows. Includes analytics, ETL, security automation, and interactive notebooks.

---

## 📁 Project Structure

```
gcp-bigdata-projects/
├── bigquery_analysis/           # SQL-based analytics on storage data
├── dataflow_pipeline/          # Apache Beam pipeline with GCS CSV
├── iam_policy_enforcement/     # IAM role restriction tool
├── notebooks/                  # BigQuery analysis in Jupyter Notebook
└── README.md
```

---

## 🧠 Project Descriptions

### 1️⃣ BigQuery Analysis
Location: `bigquery_analysis/storage_perf_query.sql`

A sample SQL query used to analyze storage device telemetry in BigQuery.
- 💡 Focus: performance and usage insights
- 📊 Output: structured analysis result of stored device records

```sql
-- Preview
SELECT model, AVG(temperature) AS avg_temp
FROM `project.dataset.telemetry`
GROUP BY model
ORDER BY avg_temp DESC
```

---

### 2️⃣ Dataflow CSV Transformation
Location: `dataflow_pipeline/gcs_csv_transform.py`

An Apache Beam pipeline using GCP Dataflow to:
- Ingest CSV from Google Cloud Storage (GCS)
- Transform selected fields
- Write output back to GCS or BigQuery

#### 🚀 To Run:
```bash
python3 gcs_csv_transform.py --input gs://your-bucket/input.csv --output gs://your-bucket/output/
```
- 💡 Dependencies: Apache Beam SDK for Python

---

### 3️⃣ IAM Policy Enforcement Tool
Location: `iam_policy_enforcement/restrict_service_account_roles.py`

This Python tool automates IAM hardening by:
- Auditing service accounts for overprivileged roles
- Removing roles not in a safe list

#### 🛡️ Use Case:
Ensure least-privilege across GCP service accounts.

#### 🚀 To Run:
```bash
python3 restrict_service_account_roles.py --project your-project-id
```

---

### 4️⃣ BigQuery Notebook Analysis
Location: `notebooks/gcp_data_analysis.ipynb`

A Jupyter notebook prototype for:
- Interactively querying BigQuery data
- Visualizing data distributions and outliers
- Annotated step-by-step SQL and result insights

#### 💡 Use:
Open with Jupyter Lab or Google Colab and connect to BigQuery.

---

## 🧑‍💻 Author
**Lisa Mary Lee**  
💼 [LinkedIn](https://www.linkedin.com/in/lisamarylee)  
📫 lisamarylee@gmail.com

---

## 📜 License
MIT License — see `LICENSE` for details.
