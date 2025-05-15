# 📊 Create a Report in Looker Studio

This lab demonstrates how to create a dynamic marketing performance report using Looker Studio and GA4 data hosted in BigQuery. You will build visualizations and scorecards that help marketing teams better understand traffic sources, user behavior, and campaign performance.

---

## 🧩 Key Objectives

- Connect Looker Studio to BigQuery
- Build a bar chart for browser usage
- Create a scorecard for unique visitors
- Visualize campaign activity using time series
- Display global visitor distribution in a table
- Apply filters and formatting for interactivity

---

## 📁 Report Structure

### 1. Browser Usage (Bar Chart)
- **Dimension**: `device.browser`
- **Metric**: `COUNT_DISTINCT(fullVisitorId)` as `Total Visitors`
- **Top 5 Browsers**

### 2. Total Visitors (Scorecard)
- Metric: `COUNT_DISTINCT(fullVisitorId)`

### 3. Jazzy July Campaign (Time Series)
- Dimension: `date`
- Metric: `COUNT_DISTINCT(hits.item.transactionId)`
- Date Range: July 1–14, 2017

### 4. Visitor Location (Table)
- Dimension: `geoNetwork.country`
- Metric: `totals.pageviews`
- Filter: Starts with `"br"` (Brazil)

---

## 📍 Notes

- **Metrics vs. Dimensions**: Metrics are numerical values, while dimensions categorize.
- **Custom Fields**: Use `Add a field` for `Total Visitors` and `Number of Transactions`.
- **Filters**: Use Advanced Filters for interactivity.

---

## 👩‍💻 Created By
**Lisa Mary Lee**  
📫 lisamarylee@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/lisamarylee)
