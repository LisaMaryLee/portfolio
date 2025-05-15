## 📄 Summary: Identify Different Batch and Streaming Data Sources  
**Project:** `gcp_batch_vs_streaming.ipynb`  
**Role:** Cloud Data Analyst, TheLook eCommerce  

In this BigQuery lab, I analyzed the differences between batch and streaming data sources by inspecting live tables, executing queries on dynamic datasets, and formatting time-based aggregations for near real-time dashboards.

---

### 🔍 Objectives
- Determine whether BigQuery tables use **streaming** or **batch** loading.
- Run time-based queries on the `shopping_cart` and `orders` tables.
- Join multiple tables to create category-specific dashboards.
- Use **timestamp formatting** and **aggregation** techniques.

---

### 🧠 Key Skills Demonstrated
- Real-time query analysis using **streaming buffers** in BigQuery
- Table inspection through the **Details** and **Streaming Statistics** tabs
- **INNER JOIN** between product metadata and transactional logs
- Time-window filtering using `TIMESTAMP_SUB()` and `CURRENT_TIMESTAMP()`
- Formatted time slicing with `FORMAT_TIMESTAMP()` for grouped analysis

---

### 🛠️ Techniques Used
- Verified live data ingestion by re-running queries and observing updates in `shopping_cart`
- Differentiated batch-only `orders` table from streaming-capable `shopping_cart`
- Filtered and grouped cart additions by **minute** using:
  ```sql
  FORMAT_TIMESTAMP("%H:%M", sc.created_at)
  ```
- Built an analytical query combining filters on product category and event time

---

### 📊 Insight Delivered
Created a real-time minute-by-minute dashboard of items (specifically `Jeans`) added to shopping carts. This enabled merchandising stakeholders to monitor pricing effectiveness and stock decisions in near real time.

---

