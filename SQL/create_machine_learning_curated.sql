DROP TABLE IF EXISTS stedi3.machine_learning_curated;

CREATE EXTERNAL TABLE stedi3.machine_learning_curated (
  user string,
  timeStamp bigint,
  x double,
  y double,
  z double,
  serialNumber string,
  sensorReadingTime bigint,
  distanceFromObject int
)
STORED AS PARQUET
LOCATION 's3://stedi-lake-house-wleed/curated/machine_learning/';