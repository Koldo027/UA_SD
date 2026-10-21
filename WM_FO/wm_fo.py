import sys
import time
import json
from kafka import KafkaProducer, KafkaConsumer

def main():
    if len(sys.argv) < 3:
        print("Uso: python wm_fo.py <Kafka_Broker> <ID_Operador>")
        sys.exit(1)

    broker = sys.argv[1]
    op_id = sys.argv[2]
    producer = KafkaProducer(bootstrap_servers=broker, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    print(f"[FO {op_id}] Conectado a Kafka. Leyendo peticiones.txt...")
    try:
        with open("WM_FO/peticiones.txt", "r") as f:
            for linea in f:
                linea = linea.strip()
                if not linea: continue
                ws_id, duracion = linea.split(",")
                orden = {"id_ws": ws_id, "duracion": int(duracion), "id_operario": op_id}

                print(f"[FO {op_id}] Solicitando riego en {ws_id} ({duracion}s)...")
                producer.send("solicitudes_riego", orden)
                producer.flush()
                time.sleep(4)
    except FileNotFoundError:
        print("No se encontro peticiones.txt")

if __name__ == "__main__":
    main()