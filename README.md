


# STEDI Human Balance Analytics

This project builds a lakehouse solution for STEDI Step Trainer sensor data using AWS S3, AWS Glue, AWS Glue Studio, Spark, and Amazon Athena.

## Project Overview

The STEDI team developed a Step Trainer device that collects motion sensor data. The companion mobile application also collects accelerometer data from users' phones.

The goal of this project is to process customer, accelerometer, and step trainer data through landing, trusted, and curated lakehouse zones. The final curated dataset is prepared for data scientists to use for machine learning.

Privacy is an important requirement in this project. Only customers who agreed to share their data for research purposes are included in the trusted and curated datasets.

## AWS Services Used

- Amazon S3
- AWS Glue
- AWS Glue Studio
- Amazon Athena
- AWS Glue Data Catalog
- Apache Spark / PySpark

## S3 Bucket



## Lakehouse Zones

### Landing Zone

The landing zone contains the raw JSON data loaded into S3.

Tables:

* `customer_landing`
* `accelerometer_landing`
* `step_trainer_landing`

### Trusted Zone

The trusted zone contains filtered and sanitized data. Only customers who agreed to share their data for research are included.

Tables:

* `customer_trusted`
* `accelerometer_trusted`
* `step_trainer_trusted`

### Curated Zone

The curated zone contains prepared datasets for analytics and machine learning.

Tables:

* `customers_curated`
* `machine_learning_curated`

## Final Row Counts

| Table                    | Count |
| ------------------------ | ----: |
| customer_landing         |   956 |
| accelerometer_landing    | 81273 |
| step_trainer_landing     | 28680 |
| customer_trusted         |   482 |
| accelerometer_trusted    | 40981 |
| customers_curated        |   482 |
| step_trainer_trusted     | 14460 |
| machine_learning_curated | 43681 |

## Data Sources

### Customer Data

Customer records were loaded into the `customer_landing` table.

Fields include:

* serialnumber
* sharewithpublicasofdate
* birthday
* registrationdate
* sharewithresearchasofdate
* customername
* email
* lastupdatedate
* phone
* sharewithfriendsasofdate

### Accelerometer Data

Accelerometer records were loaded into the `accelerometer_landing` table.

Fields include:

* timeStamp
* user
* x
* y
* z

### Step Trainer Data

Step trainer records were loaded into the `step_trainer_landing` table.

Fields include:

* sensorReadingTime
* serialNumber
* distanceFromObject

## Transformations

### customer_trusted

The `customer_trusted` table was created by filtering customer records from the landing zone.

Only customers who agreed to share their data for research were included.

Filter condition:

```sql
sharewithresearchasofdate IS NOT NULL
```

Expected row count:

```text
482
```

### accelerometer_trusted

The `accelerometer_trusted` table was created by joining accelerometer records with trusted customers.

Join condition:

```sql
accelerometer_landing.user = customer_trusted.email
```

This ensures that only accelerometer readings from customers who agreed to share their data for research are included.

Expected row count:

```text
40981
```

### customers_curated

The `customers_curated` table was created from trusted customers.

It includes only customers who:

1. Agreed to share their data for research.
2. Have accelerometer data.

Join condition:

```sql
customer_trusted.email = accelerometer_trusted.user
```

Expected row count:

```text
482
```

### step_trainer_trusted

The `step_trainer_trusted` table was created by filtering step trainer records using the serial numbers from `customers_curated`.

The project notes explain that a normal inner join can produce incorrect results in Glue because the serial number is not unique. Therefore, the filtering was done using an `IN` condition.

Logic used:

```sql
SELECT
  s.sensorReadingTime,
  s.serialNumber,
  s.distanceFromObject
FROM step_trainer_landing s
WHERE s.serialNumber IN (
  SELECT DISTINCT c.serialnumber
  FROM customers_curated c
)
```

Expected row count:

```text
14460
```

### machine_learning_curated

The `machine_learning_curated` table was created by joining accelerometer trusted data with step trainer trusted data using matching timestamps.

Join condition:

```sql
accelerometer_trusted.timeStamp = step_trainer_trusted.sensorReadingTime
```

This final table contains the combined sensor and accelerometer readings needed for machine learning.

Expected row count:

```text
43681
```

## Final Validation Query

The following Athena query was used to validate the final row counts:

```sql
SELECT 'customer_landing' AS table_name, COUNT(*) AS row_count FROM customer_landing
UNION ALL
SELECT 'accelerometer_landing' AS table_name, COUNT(*) AS row_count FROM accelerometer_landing
UNION ALL
SELECT 'step_trainer_landing' AS table_name, COUNT(*) AS row_count FROM step_trainer_landing
UNION ALL
SELECT 'customer_trusted' AS table_name, COUNT(*) AS row_count FROM customer_trusted
UNION ALL
SELECT 'accelerometer_trusted' AS table_name, COUNT(*) AS row_count FROM accelerometer_trusted
UNION ALL
SELECT 'customers_curated' AS table_name, COUNT(*) AS row_count FROM customers_curated
UNION ALL
SELECT 'step_trainer_trusted' AS table_name, COUNT(*) AS row_count FROM step_trainer_trusted
UNION ALL
SELECT 'machine_learning_curated' AS table_name, COUNT(*) AS row_count FROM machine_learning_curated;
```

## Project Structure

```text
stedi-human-balance-analytics/
│
├── sql/
│   ├── customer_landing.sql
│   ├── accelerometer_landing.sql
│   ├── step_trainer_landing.sql
│   ├── create_customer_trusted.sql
│   ├── create_accelerometer_trusted.sql
│   ├── create_customers_curated.sql
│   ├── create_step_trainer_trusted.sql
│   └── create_machine_learning_curated.sql
│
├── glue_jobs/
│   ├── customer_landing_to_trusted.py
│   ├── accelerometer_landing_to_trusted.py
│   ├── customer_trusted_to_curated.py
│   ├── step_trainer_landing_to_trusted.py
│   └── machine_learning_curated.py
│
├── screenshots/
│   ├── customer_landing.png
│   ├── accelerometer_landing.png
│   ├── step_trainer_landing.png
│   ├── customer_trusted.png
│   ├── accelerometer_trusted.png
│   ├── customers_curated.png
│   ├── step_trainer_trusted.png
│   ├── machine_learning_curated.png
│   └── final_counts.png
│
└── README.md
```

## Notes

Some Glue jobs were configured to read directly from S3 instead of the Glue Data Catalog to avoid IAM and Lake Formation permission issues in the lab environment.

AWS Glue Studio SQL Query nodes were used whenever possible because they provide more reliable results for this project than normal join transform nodes.

Before rerunning any Glue job, the existing Athena table and old S3 output files were deleted to avoid duplicate or stale results.

```
```
