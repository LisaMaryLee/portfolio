
# Creating a BigQuery Authorized View

## Overview
This lab demonstrates how to use BigQuery Authorized Views to control dataset access. Authorized Views allow granular access controls, enabling analysts to access only specific rows or columns of data.

## Objectives
- Set permissions on BigQuery datasets.
- Create Authorized Views for read-only subsets of data.
- Use `SESSION_USER()` to restrict row-level access.

---

## Task 1: Create the Source Dataset

### Steps:
1. Create dataset `source_data`.
2. Load table `events` using:
   ```bash
   bq load --autodetect $DEVSHELL_PROJ:source_data.events gs://cloud-training/gcpsec/labs/bq-authviews-source.csv
   ```
3. Update user info:
   ```sql
   UPDATE source_data.events
   SET email= '"USERNAME2"'
   WHERE email='rhonda.burns@example-dev.com'
   ```

---

## Task 2: Create the Analyst Dataset

### Steps:
1. Create dataset `analyst_views`.
2. Create redacted view `no_user_info`:
   ```sql
   SELECT date, type, company, call_duration, call_type,
          call_num_users, call_os, rating, comment,
          session_id, dialin_duration, ticket_number, ticket_driver
   FROM `PROJECT_ID.source_data.events`
   ```

3. Create row-filtered view `row_filter_session_user`:
   ```sql
   SELECT *
   FROM `PROJECT_ID.source_data.events`
   WHERE email = SESSION_USER()
   ```

---

## Task 3: Secure the Analyst Dataset

- Grant `BigQuery Data Viewer` role to Username 2 on `analyst_views`.

---

## Task 4: Secure the Source Dataset

- Remove `BigQuery Data Viewer` role from `source_data`.
- Authorize the views `no_user_info` and `row_filter_session_user` to access `source_data`.

---

## Task 5: Test Security Settings

### As Username 2:
- ✅ Query `analyst_views.no_user_info`
- ✅ Query `analyst_views.row_filter_session_user` (only sees 68 user-specific rows)
- ❌ Query `source_data.events` (access denied)

---

## Summary

- Views allow selective column/row exposure.
- `SESSION_USER()` enables row-level security by email.
- Source dataset access is locked down to only authorized views.

