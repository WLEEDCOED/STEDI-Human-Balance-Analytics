DROP TABLE IF EXISTS stedi3.customer_trusted;

CREATE EXTERNAL TABLE stedi3.customer_trusted (
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
LOCATION 's3://stedi-lake-house-wleed/trusted/customer/';