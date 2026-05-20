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

# Read directly from S3, not from Glue Data Catalog
input_path = "s3://stedi-lake-house-wleed/landing/customer/"
output_path = "s3://stedi-lake-house-wleed/trusted/customer/"

df = spark.read.json(input_path)

customer_trusted = df.filter(df["sharewithresearchasofdate"].isNotNull())

customer_trusted.write.mode("overwrite").parquet(output_path)

job.commit()