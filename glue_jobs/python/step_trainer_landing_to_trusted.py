import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
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

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node step_trainer_landing
step_trainer_landing_node1779291614099 = glueContext.create_dynamic_frame.from_options(format_options={"multiLine": "false"}, connection_type="s3", format="json", connection_options={"paths": ["s3://stedi-lake-house-wleed/landing/step_trainer/"], "recurse": True}, transformation_ctx="step_trainer_landing_node1779291614099")

# Script generated for node customers_curated
customers_curated_node1779291762990 = glueContext.create_dynamic_frame.from_options(format_options={}, connection_type="s3", format="parquet", connection_options={"paths": ["s3://stedi-lake-house-wleed/curated/customer/"], "recurse": True}, transformation_ctx="customers_curated_node1779291762990")

# Script generated for node SQL Query
SqlQuery0 = '''
SELECT
  s.sensorReadingTime,
  s.serialNumber,
  s.distanceFromObject
FROM step_trainer_landing s
WHERE s.serialNumber IN (
  SELECT DISTINCT c.serialnumber
  FROM customers_curated c
)
'''
SQLQuery_node1779291823613 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"step_trainer_landing":step_trainer_landing_node1779291614099, "customers_curated":customers_curated_node1779291762990}, transformation_ctx = "SQLQuery_node1779291823613")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=SQLQuery_node1779291823613, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1779288845041", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1779291858113 = glueContext.write_dynamic_frame.from_options(frame=SQLQuery_node1779291823613, connection_type="s3", format="glueparquet", connection_options={"path": "s3://stedi-lake-house-wleed/trusted/step_trainer/", "partitionKeys": []}, format_options={"compression": "snappy"}, transformation_ctx="AmazonS3_node1779291858113")

job.commit()
