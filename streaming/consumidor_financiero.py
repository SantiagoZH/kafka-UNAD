from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window
from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType, TimestampType

schema = StructType([
    StructField("simbolo", StringType()),
    StructField("precio", FloatType()),
    StructField("cantidad", IntegerType()),
    StructField("timestamp", TimestampType())
])

spark = SparkSession.builder.appName("StreamingBolsa").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "transacciones").load()

parsed_df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

stats = parsed_df.groupBy(window(col("timestamp"), "1 minute"), "simbolo") \
    .agg({"precio": "avg", "cantidad": "sum"})

query = stats.writeStream.outputMode("complete").format("console").start()
query.awaitTermination()
