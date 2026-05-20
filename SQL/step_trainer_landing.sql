CREATE EXTERNAL TABLE IF NOT EXISTS stedi3.step_trainer_landing (
  sensorReadingTime bigint,
  serialNumber string,
  distanceFromObject int
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://stedi-lake-house-wleed/landing/step_trainer/';