## 📄 Summary: Practice Transformation Methods  
**Project:** `gcp_transformation_methods.ipynb`  
**Role:** Cloud Data Analyst, TheLook eCommerce  

In this lab, I practiced foundational transformation techniques using SQL in BigQuery to explore data and improve data quality. These methods support exploratory data analysis (EDA) by preparing data for deeper analytics, filtering inconsistencies, and summarizing key metrics.

---

### 🔍 Objectives
- Use `LIMIT` to preview datasets efficiently
- Apply `COUNT(DISTINCT ...)` to detect duplicate values
- Use `GROUP BY` and `HAVING` to summarize and filter categorical data
- Sample data randomly with `TABLESAMPLE`
- Aggregate purchase data to identify top-value customers

---

### 🧠 Key Skills Demonstrated
- SQL querying for dataset exploration
- Identification of data duplication using `COUNT(*)` vs. `COUNT(DISTINCT)`
- Group-wise aggregation and filtering using `GROUP BY` + `HAVING`
- Efficient data sampling using `TABLESAMPLE SYSTEM`
- Value-based ranking through `SUM(...)` and `ORDER BY DESC`

---

### 🛠️ Techniques Used
- Assessed data quality by comparing total vs. distinct product names
- Identified item counts per category and segment
- Applied thresholds using `HAVING` to isolate large categories
- Sampled 10% of the `products` table for fast prototyping:
  ```sql
  SELECT * FROM thelook_ecommerce.products TABLESAMPLE SYSTEM (10 PERCENT)
  ```
- Aggregated order totals to find top-spending users

---

### 📊 Insight Delivered
These transformation techniques provided a clearer view of product duplication, inventory distribution, and high-value customers. This approach empowered better product management and improved the accuracy of return-related reporting for cross-functional teams.

---
