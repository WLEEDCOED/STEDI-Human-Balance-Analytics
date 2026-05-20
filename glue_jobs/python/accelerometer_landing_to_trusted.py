import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions

args = getResolvedOptions(sys.argv, ["JOB_NAME"])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args["JOB_NAME"], args)

accelerometer_path = "s3://stedi-lake-house-wleed/landing/accelerometer/"
customer_trusted_path = "s3://stedi-lake-house-wleed/trusted/customer/"
output_path = "s3://stedi-lake-house-wleed/trusted/accelerometer/"

a = spark.read.json(accelerometer_path)
c = spark.read.parquet(customer_trusted_path)

accelerometer_trusted = a.join(
    c,
    a["user"] == c["email"],
    "inner"
).select(a["timeStamp"], a["user"], a["x"], a["y"], a["z"])

accelerometer_trusted.write.mode("overwrite").parquet(output_path)

job.commit()