# Proyecto de Streaming Financiero con Kafka y PySpark

## Descripción General
Sistema de procesamiento en tiempo real de transacciones bursátiles utilizando Apache Kafka como broker de mensajes y PySpark para análisis de datos en streaming.

## Arquitectura del Proyecto

```
┌─────────────┐     ┌──────────┐     ┌──────────────────┐
│  Productor  │────▶│  Kafka   │────▶│  Consumidor      │
│  (Topics)   │     │ Broker   │     │  (PySpark)       │
└─────────────┘     └──────────┘     └──────────────────┘
                       :9092               Agregación
                                       y Análisis en Vivo
```

## Componentes del Servidor

### 1. **Kafka Broker** (`localhost:9092`)
- **Función**: Actúa como intermediario de mensajes
- **Topic**: `transacciones`
- **Responsabilidad**: Recibir y distribuir mensajes de transacciones bursátiles

### 2. **Productor de Datos** 
- Envía datos JSON con la estructura:
```json
{
  "simbolo": "AAPL",
  "precio": 150.25,
  "cantidad": 100,
  "timestamp": "2026-04-14T10:30:00"
}
```

### 3. **Consumidor Financiero** (`consumidor_financiero.py`)
- **Puerto**: Lee del topic de Kafka
- **Procesamiento**:
  - Parsea mensajes JSON usando el schema definido
  - Agrupa datos por ventanas de 1 minuto
  - Calcula estadísticas por símbolo bursátil
  - Muestra resultados en consola en tiempo real

## Flujo de Datos Paso a Paso

### Paso 1: Lectura desde Kafka
```python
df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "transacciones").load()
```
- Conecta con el broker Kafka en el puerto 9092
- Se suscribe al topic "transacciones"
- Lee datos de forma continua y sin bloqueos

### Paso 2: Parseo de Datos
```python
parsed_df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")
```
- Convierte el valor JSON en string
- Lo deserializa usando el schema predefinido
- Extrae campos individuales: símbolo, precio, cantidad, timestamp

### Paso 3: Agregación con Ventanas de Tiempo
```python
stats = parsed_df.groupBy(window(col("timestamp"), "1 minute"), "simbolo") \
    .agg({"precio": "avg", "cantidad": "sum"})
```
- Crea ventanas deslizantes de 1 minuto
- Agrupa transacciones por símbolo dentro de cada ventana
- Calcula:
  - Precio promedio por símbolo
  - Cantidad total transaccionada

### Paso 4: Salida en Consola
```python
query = stats.writeStream.outputMode("complete").format("console").start()
query.awaitTermination()
```
- Modo "complete": muestra todos los resultados cada intervalo
- Imprime resultados formateados en consola
- Se mantiene ejecutándose hasta interrumpirse

## Instalación y Configuración

### Requisitos
- Python 3.8+
- Apache Kafka
- PySpark 3.x
- Windows (según tu setup actual)

### Pasos de Instalación

1. **Iniciar Zookeeper** (requerido por Kafka):
```bash
Iniciar ZooKeeper: sudo /opt/Kafka/bin/zookeeper-server-start.sh /opt/Kafka/config/zookeeper.properties &
```

2. **Iniciar Kafka Broker**:
```bash
Iniciar Kafka: sudo /opt/Kafka/bin/kafka-server-start.sh /opt/Kafka/config/server.properties &
```

3. **Crear el topic "transacciones"**:
```bash
Crear Topic: /opt/Kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic transacciones
```

4. **Ejecutar el productor**:
```bash
python3 productor_financiero.py
```
5. **Ejecutar el consumidor**:
```bash
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3 consumidor_financiero.py
```

## Ejemplo de Salida

```
Batch: 0
+------------------------------------------+--------+---------+-----------+
|                   window                 |simbolo | avg(precio) | sum(cantidad)|
+------------------------------------------+--------+---------+-----------+
|[2026-04-14 10:30:00, 2026-04-14 10:31:00]| AAPL   | 150.50  | 5000      |
|[2026-04-14 10:30:00, 2026-04-14 10:31:00]| GOOGL  | 140.25  | 3200      |
+------------------------------------------+--------+---------+-----------+
```


## Troubleshooting

**Error: "Kafka broker no disponible"**
- Verifica que Zookeeper y Kafka estén corriendo en los puertos correctos

**Error: "Topic no encontrado"**
- Asegúrate de crear el topic antes de producir/consumir

**Error: "Schema no coincide"**
- Valida que los mensajes JSON tengan exactamente la estructura esperada

---
**Última actualización**: Abril 14, 2026