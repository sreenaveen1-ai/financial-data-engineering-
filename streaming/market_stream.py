from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType


spark = (
    SparkSession.builder
    .appName("FinancialMarketStreaming")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


schema = StructType([
    StructField("symbol", StringType(), True),
    StructField("price", DoubleType(), True),
    StructField("volume", IntegerType(), True),
    StructField("timestamp", StringType(), True),
])


raw_stream = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "market-data")
    .option("startingOffsets", "earliest")
    .load()
)


json_stream = raw_stream.select(
    from_json(
        col("value").cast("string"),
        schema
    ).alias("data")
).select("data.*")


query = (
    json_stream.writeStream
    .format("console")
    .outputMode("append")
    .option("truncate", "false")
    .start()
)

query.awaitTermination()