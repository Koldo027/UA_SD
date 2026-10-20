import socket
import sys
import time
from common.sockets_protocol import build_msg, parse_msg

hay_fuga = False

def hilo_servidor_engine(puerto_engine, ws_id, ip_central, puerto_central):
    global hay_fuga
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.bind(('0.0.0.0', puerto_engine))
    srv.listen(1)
    print(f"[{ws_id}-M] Esperando conexion local del Engine en puerto {puerto_engine}...")
    conn, addr = srv.accept()
    print(f"[{ws_id}-M] Engine conectado.")

    while True:
        time.sleep(1)
        try:
            conn.send(empaquetr("HEALTH_CHECK").encode('utf-8'))
            conn.settimeout(2.0)
            raw = conn.recv(1024).decode('utf-8')
            resp = desempaquetar(raw)

            if not resp or resp == "KO":
                if not hay_fuga:
                    print(f"[{ws_id}-M] Fallo en Engine detectado. Reportando a Central...")
                    reportar_fuga_a_central(ws_id, ip_central, puerto_central)
                    hay_fuga = True
            else:
                hay_fuga = False
        except socket.timout:
            if not hay_fuga:
                print(f"[{ws_id}-M] Timeout con Engine. Avisando a Central...")
                reportar_fuga_a_central(ws_id, ip_central, puerto_central)
                hay_fuga = True

def reportar_fuga_a_central(ws_id, ip, puerto):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, puerto))
        s.send(empaquetar(f"ALERTA_FUGA#{ws_id}").encode('utf-8'))
        s.close()
    except Exception as e:
        print(f"[{ws_id}-M] Imposible conectar con WM_Central: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python wm_ws_m.py <Puerto_Engine> <Central_IP>:<Central_Port> <ID_WS>")
        sys.exit(1)

    central_ip, central_port = sys.argv[2].split(":")
    ws_id = sys.argv[3]

    run_monitor(central_ip, int(central_port), ws_id)