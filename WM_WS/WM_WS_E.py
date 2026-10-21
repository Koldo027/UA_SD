import socket
import sys
import threading
from sockets_protocol import empaquetar, desempaquetar

simular_fuga = False

def escuchar_teclado():
    global simular_fuga
    while True:
        tecla = input()
        if tecla.strip().lower() == "k":
            simular_fuga = not simular_fuga
            print(f"[ENGINE] Modo fuga/fallo cambiado a: {simular_fuga}")

def main():
    if len(sys.argv) < 3:
        print("Uso: python WM_WS_E.py <Kafka_Broker> <Monitor_IP:Puerto>")
        sys.exit(1)

    mon_ip, mon_port = sys.argv[2].split(":")

    threading.Thread(target=escuchar_teclado, daemon=True).start()
    print("[ENGINE] Pulsa 'k' + Enter en cualquier momento para simular/quitar un fallo.")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((mon_ip, int(mon_port)))
    print("[ENGINE] Conectado al Monitor.")

    while True:
        raw = s.recv(1024).decode('utf-8')
        if not raw:
            break
        msg = desempaquetar(raw)
        if msg == "HEALTH_CHECK":
            resp = "KO" if simular_fuga else "OK"
            s.send(empaquetar(resp).encode('utf-8'))

if __name__ == "__main__":
    main()