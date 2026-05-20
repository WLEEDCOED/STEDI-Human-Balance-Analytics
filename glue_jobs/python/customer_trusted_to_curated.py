import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node customer_trusted
customer_trusted_node1779291141441 = glueContext.create_dynamic_frame.from_options(format_options={}, connection_type="s3", format="parquet", connection_options={"paths": ["s3://stedi-lake-house-wleed/trusted/customer/"], "recurse": True}, transformation_ctx="customer_trusted_node1779291141441")

# Script generated for node accelerometer_trusted
accelerometer_trusted_node1779291224544 = glueContext.create_dynamic_frame.from_options(format_options={}, connection_type="s3", format="parquet", connection_options={"paths": ["s3://stedi-lake-house-wleed/trusted/accelerometer/"], "recurse": True}, transformation_ctx="accelerometer_trusted_node1779291224544")

# Script generated for node SQL Query
SqlQuery0 = '''
SELECT DISTINCT
  c.serialnumber,
  c.sharewithpublicasofdate,
  c.birthday,
  c.registrationdate,
  c.sharewithresearchasofdate,
  c.customername,
  c.email,
  c.lastupdatedate,
  c.phone,
  c.sharewithfriendsasofdate
FROM customer_trusted c
JOIN accelerometer_trusted a
ON c.email = a.user

'''
SQLQuery_node1779291262120 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"accelerometer_trusted":accelerometer_trusted_node1779291224544, "customer_trusted":customer_trusted_node1779291141441}, transformation_ctx = "SQLQuery_node1779291262120")

# Script generated for node Amazon S3
AmazonS3_node1779291344096 = glueContext.write_dynamic_frame.from_options(frame=SQLQuery_node1779291262120, connection_type="s3", format="glueparquet", connection_options={"path": "s3://stedi-lake-house-wleed/curated/customer/", "partitionKeys": []}, format_options={"compression": "snappy"}, transformation_ctx="AmazonS3_node1779291344096")

job.commit()