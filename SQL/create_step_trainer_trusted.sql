DROP TABLE IF EXISTS stedi3.step_trainer_trusted;

CREATE EXTERNAL TABLE stedi3.step_trainer_trusted (
  sensorReadingTime bigint,
  serialNumber string,
  distanceFromObject int
)
STORED AS PARQUET
LOCATION 's3://stedi-lake-house-wleed/trusted/step_trainer/';