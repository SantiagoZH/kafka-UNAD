import time, json, random
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

print("Enviando transacciones en tiempo real...")
while True:
    datos = {
        "simbolo": random.choice(['AAPL', 'GOOGL', 'AMZN', 'MSFT', 'TSLA']),
        "precio": round(random.uniform(100, 1500), 2),
        "cantidad": random.randint(1, 50),
        "timestamp": int(time.time())
    }
    producer.send('transacciones', value=datos)
    print(f"Enviado: {datos}")
    time.sleep(1)
