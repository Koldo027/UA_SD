# central/wm_central.py
import socket
import threading
import sys
from common.sockets_protocol import parse_msg, build_msg
from WM_Central.db_manager import init_db, registrar_estacion, actualizar_estado, obtener_estaciones

VERDE = "\033[92m"
ROJO = "\033[91m"
NARANJA = "\033[93m"
GRIS = "\033[90m"
RESET = "\033[0m"

def imprimir_panel():
    estaciones = obtener_estaciones()
    print("\n [Central] Panel de monitorización de riego \n")
    for id_ws, ubi, est, caud, vol in estaciones:
        color = GRIS
        if est == "DISPONIBLE": color = VERDE
        elif est == "REGANDO": color = VERDE
        elif est == "AVERIA" or est == "FUGA": color = ROJO
        elif est == "FUERA_SERVICIO": color = NARANJA

        print(f"WS: {id_ws:<6} | Ubic: {ubi:<15} | Estado: {color}{est:<15}{RESET} | Caudal: {caud} L/min")
    print("="*50 + "\n")

def handle_monitor_client(conn, addr):
    print(f"[CENTRAL] Nueva conexión desde {addr}")
    try:
        data = conn.recv(1024).decode('utf-8')
        if data:
            parts = parse_msg(data)
            if parts[0] == "REGISTRO":
                ws_id, location = parts[1], parts[2]
                print(f"[CENTRAL] Registrando Estación {ws_id} en {location}")
                response = build_msg("STATUS", "OK", "Estacion registrada correctamente")
                conn.send(response.encode('utf-8'))
    except Exception as e:
        print(f"[CENTRAL] Error con {addr}: {e}")
    finally:
        conn.close()

def start_socket_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen()
    print(f"[CENTRAL] Servidor Socket a la escucha en puerto {port}...")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_monitor_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python wm_central.py <Puerto_Socket> <Kafka_Broker>")
        sys.exit(1)

    port = int(sys.argv[1])
    kafka_broker = sys.argv[2]

    socket_thread = threading.Thread(target=start_socket_server, args=(port,))
    socket_thread.daemon = True
    socket_thread.start()

    socket_thread.join()