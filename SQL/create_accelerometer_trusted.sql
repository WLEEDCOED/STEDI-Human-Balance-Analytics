DROP TABLE IF EXISTS stedi3.accelerometer_trusted;

CREATE EXTERNAL TABLE stedi3.accelerometer_trusted (
  timeStamp bigint,
  user string,
  x double,
  y double,
  z double
)
STORED AS PARQUET
LOCATION 's3://stedi-lake-house-wleed/trusted/accelerometer/';