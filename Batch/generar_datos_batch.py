import pandas as pd
import random
from datetime import datetime, timedelta

data = []
acciones = ['AAPL', 'GOOGL', 'AMZN', 'MSFT', 'TSLA']
fecha_base = datetime(2024, 1, 1)

for i in range(1000):
    data.append({
        "simbolo": random.choice(acciones),
        "precio": round(random.uniform(100, 1500), 2),
        "cantidad": random.randint(1, 100),
        "fecha": (fecha_base + timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d')
    })

df = pd.DataFrame(data)
df.to_csv('datos_historicos_bolsa.csv', index=False)
print("Archivo 'datos_historicos_bolsa.csv' creado.")
