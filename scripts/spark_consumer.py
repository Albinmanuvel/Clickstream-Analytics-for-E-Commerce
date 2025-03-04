from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, count
from pyspark.sql.types import StructType, StructField, StringType, TimestampType

# Define schema for incoming JSON data
schema = StructType([
    StructField("user_id", StringType(), True),
    StructField("event_type", StringType(), True),
    StructField("timestamp", TimestampType(), True),
    StructField("product_id", StringType(), True),
    StructField("session_id", StringType(), True)
])

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Clickstream Data Consumer") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.elasticsearch:elasticsearch-spark-30_2.12:8.2.0") \
    .getOrCreate()

# Read data from Kafka
kafka_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "clickstream_topic") \
    .option("startingOffsets", "latest") \
    .load()

# Parse the JSON messages from Kafka
parsed_df = kafka_df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Aggregate user sessions (example: total events per session)
session_agg_df = parsed_df \
    .groupBy("session_id") \
    .agg(count("event_type").alias("total_events"))

# Write to Elasticsearch
query = session_agg_df \
    .writeStream \
    .format("org.elasticsearch.spark.sql") \
    .option("es.nodes", "localhost") \
    .option("es.port", "9200") \
    .option("checkpointLocation", "checkpoint/") \
    .option("es.resource", "clickstream_data/_doc") \
    .outputMode("update") \
    .start()

query.awaitTermination()


session_agg_df.writeStream \
    .outputMode("update") \
    .foreachBatch(lambda batchDF, batchId: batchDF.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://localhost:5432/clickstream_db") \
        .option("dbtable", "clickstream_sessions") \
        .option("user", "your_username") \
        .option("password", "your_password") \
        .option("driver", "org.postgresql.Driver") \
        .save()) \
    .start()
