from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, sum, round as spark_round

spark = SparkSession.builder.appName("AnalisisBatchBolsa").getOrCreate()

df = spark.read.csv("datos_historicos_bolsa.csv", header=True, inferSchema=True)

df_limpio = df.filter(col("cantidad") > 10)

# 3. Transformación y Análisis
resultado = df_limpio.groupBy("simbolo").agg(
    spark_round(avg("precio"), 2).alias("precio_prom"),
    sum("cantidad").alias("volumen_total")
).orderBy(col("volumen_total").desc())

print("\n" + "="*40)
print("   RESULTADOS DEL ANÁLISIS BATCH")
print("="*40)
resultado.show()

print("DISTRIBUCIÓN VISUAL DEL VOLUMEN:")
rows = resultado.collect()
max_vol = max([row['volumen_total'] for row in rows])
for row in rows:
    bar = "#" * int((row['volumen_total'] / max_vol) * 20)
    print(f"{row['simbolo']}: {bar} ({row['volumen_total']})")

spark.stop()
