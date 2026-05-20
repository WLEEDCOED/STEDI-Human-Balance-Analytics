DROP TABLE IF EXISTS stedi3.customers_curated;

CREATE EXTERNAL TABLE stedi3.customers_curated (
  serialnumber string,
  sharewithpublicasofdate bigint,
  birthday string,
  registrationdate bigint,
  sharewithresearchasofdate bigint,
  customername string,
  email string,
  lastupdatedate bigint,
  phone string,
  sharewithfriendsasofdate bigint
)
STORED AS PARQUET
LOCATION 's3://stedi-lake-house-wleed/curated/customer/';