## 📄 Summary: Apply RFM Method to Segment Customer Data  
**Project:** `gcp_rfm_segmentation.ipynb`  
**Role:** Cloud Data Analyst, TheLook eCommerce  

This lab demonstrates how to apply the Recency-Frequency-Monetary (RFM) method using BigQuery to segment customers based on purchasing behavior. The RFM segmentation supports targeted marketing strategies by identifying loyal, high-value, at-risk, and persuadable customers.

---

### 🔍 Objectives
- Explore customer and order data from the `thelook_ecommerce` dataset
- Calculate Recency using `DATE_DIFF()` and most recent order timestamps
- Count Frequency of orders per customer using `COUNT()`
- Sum Monetary value of purchases using `SUM(sale_price)`
- Build CTEs to organize intermediate computations
- Apply `NTILE(4)` for quartile-based segmentation
- Use `CASE` logic to assign customer segments based on quantiles

---

### 🧠 Key Skills Demonstrated
- SQL-based customer segmentation in BigQuery
- Joining multiple datasets (`orders` and `order_items`) to aggregate purchase behavior
- Creation of layered Common Table Expressions (CTEs)
- Use of analytical functions like `NTILE()` for quantile calculation
- Conditional logic with `CASE` to classify customer segments

---

### 🛠️ Techniques Used
- Calculated **recency** of last purchase:
  ```sql
  DATE_DIFF(CURRENT_TIMESTAMP(), MAX(created_at), DAY)
  ```
- Measured **frequency** using `COUNT(order_id)`
- Summed **monetary** value using `SUM(sale_price)`
- Structured multi-step analysis with nested `WITH` clauses (CTEs)
- Assigned segment labels like:
  - High Value Customer
  - Loyal Customer
  - At Risk Customer
  - Persuadable Customer

---

### 📊 Insight Delivered
Segmented customers based on behavior to inform targeted marketing decisions. Enabled Martina's team to focus on loyalty campaigns, re-engagement strategies, and upsell efforts using statistically grounded RFM scoring.

---
