CREATE EXTERNAL TABLE IF NOT EXISTS stedi3.accelerometer_landing (
  timeStamp bigint,
  user string,
  x double,
  y double,
  z double
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://stedi-lake-house-wleed/landing/accelerometer/';