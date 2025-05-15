## 📄 Summary: Creating and Managing SQL Pipelines  
**Project:** `gcp_sql_pipeline.ipynb`  
**Role:** Cloud Data Analyst, TheLook eCommerce  

This lab focused on building and managing a SQL-based data pipeline using BigQuery. The project involved defining table schemas, transforming geographic data using spatial SQL functions, and organizing transformations into a reusable stored procedure to meet dynamic business needs in logistics and fulfillment.

---

### 🔍 Objectives
- Create datasets and define schemas for fulfillment and location-based data
- Load and transform customer and distribution center data using geospatial functions
- Calculate customer-to-center distances using `ST_GEOGPOINT()` and `ST_DISTANCE()`
- Create and execute a stored procedure to formalize pipeline operations

---

### 🧠 Key Skills Demonstrated
- BigQuery schema creation and data ingestion
- Use of **geography data types** and **spatial SQL**
- Scalar subqueries and distance calculations
- Stored procedure creation with `CREATE PROCEDURE ... BEGIN ... END`
- Best practices in SQL pipeline maintainability and reuse

---

### 🛠️ Techniques Used
- Created `customers`, `centers`, and `product_orders_fulfillment` tables with defined schemas
- Transformed raw lat/lon data into geographic points with `ST_GEOGPOINT()`
- Calculated customer proximity to distribution centers using `ST_DISTANCE()`
- Encapsulated logic and transformation into a stored procedure:
  ```sql
  CREATE OR REPLACE PROCEDURE thelook_ecommerce.sp_create_load_tables() BEGIN ...
  ```
- Explored how to configure **scheduled queries** for regular updates

---

### 📊 Insight Delivered
A flexible and scalable SQL pipeline was created to support logistics optimization for TheLook eCommerce. The pipeline enables rapid recalculation of proximity between customers and distribution centers, supporting decisions around transportation, fulfillment speed, and location planning.

---
