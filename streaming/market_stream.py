from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    avg,
    col,
    count,
    max,
    min,
    sum,
    window,
)

spark = (
    SparkSession.builder
    .appName("FinancialMarketGold")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")


silver_stream = (
    spark.readStream
    .schema(
        """
        symbol STRING,
        price DOUBLE,
        volume INT,
        event_timestamp TIMESTAMP,
        processed_timestamp TIMESTAMP
        """
    )
    .json("data/silver/market-data")
)


gold_stream = (
    silver_stream
    .withWatermark("event_timestamp", "1 minute")

    .groupBy(
        window(col("event_timestamp"), "1 minute"),
        col("symbol")
    )
    .agg(
        avg("price").alias("avg_price"),
        min("price").alias("min_price"),
        max("price").alias("max_price"),
        sum("volume").alias("total_volume"),
        count("*").alias("tick_count"),
    )
)


query = (
    gold_stream.writeStream
    .format("json")
    .outputMode("append")
    .option("path", "data/gold/market-summary")
    .option("checkpointLocation", "data/gold/.checkpoint")
    .start()
)

query.awaitTermination()