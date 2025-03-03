from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, expr, count
from pyspark.sql.types import StructType, StringType, IntegerType, TimestampType
from pyspark.ml.recommendation import ALS
from pyspark.sql import functions as F
import psycopg2
import os

# PostgreSQL connection details
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "clickstream_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "your_username")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "your_password")

# Create Spark session
spark = SparkSession.builder \
    .appName("RealTimeProductRecommendation") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,org.postgresql:postgresql:42.2.20") \
    .getOrCreate()

# Define schema for Kafka messages
clickstream_schema = StructType([
    StructType().add("user_id", IntegerType()) \
    .add("event_type", StringType()) \
    .add("product_id", IntegerType()) \
    .add("event_timestamp", TimestampType()) \
    .add("session_id", StringType())
])

# Read data from Kafka topic
clickstream_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "clickstream_events") \
    .option("startingOffsets", "latest") \
    .load()

# Deserialize JSON data
clickstream_df = clickstream_df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), clickstream_schema).alias("data")) \
    .select("data.*")

# Filter only "purchase" or "add_to_cart" events for recommendation generation
filtered_events = clickstream_df.filter((col("event_type") == "purchase") | (col("event_type") == "add_to_cart"))

# Generate product recommendation using collaborative filtering (ALS model)
user_product_interactions = filtered_events.groupBy("user_id", "product_id").agg(count("event_type").alias("interaction_count"))

als = ALS(
    maxIter=10,
    regParam=0.1,
    userCol="user_id",
    itemCol="product_id",
    ratingCol="interaction_count",
    coldStartStrategy="drop"
)

# Train ALS model
als_model = als.fit(user_product_interactions)

# Generate top 3 product recommendations per user
recommendations = als_model.recommendForAllUsers(3)

# Flatten recommendation structure
recommendations = recommendations.selectExpr("user_id", "explode(recommendations) as rec") \
    .select(col("user_id"), col("rec.product_id").alias("recommended_product_id"), col("rec.rating").alias("confidence_score"))

# Function to write recommendations to PostgreSQL
def write_to_postgres(df, epoch_id):
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )
    cursor = conn.cursor()
    
    for row in df.collect():
        cursor.execute("""
            INSERT INTO product_recommendations (user_id, recommended_product_id, confidence_score)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, recommended_product_id) DO UPDATE 
            SET confidence_score = EXCLUDED.confidence_score;
        """, (row.user_id, row.recommended_product_id, row.confidence_score))

    conn.commit()
    cursor.close()
    conn.close()

# Write recommendations to PostgreSQL
recommendations.writeStream \
    .foreachBatch(write_to_postgres) \
    .outputMode("update") \
    .start() \
    .awaitTermination()
