import socket
import sys
import time
from common.sockets_protocol import build_msg, parse_msg

def run_monitor(central_ip, central_port, ws_id, location="River Park"):
    try:
        central_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        central_sock.connect((central_ip, central_port))
        
        reg_msg = build_msg("REGISTRO", ws_id, location)
        central_sock.send(reg_msg.encode('utf-8'))
        
        response = central_sock.recv(1024).decode('utf-8')
        print(f"[MONITOR {ws_id}] Respuesta de Central: {response}")
        central_sock.close()
    except Exception as e:
        print(f"[MONITOR {ws_id}] Error conectando a Central: {e}")
        return

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python wm_ws_m.py <Puerto_Engine> <Central_IP>:<Central_Port> <ID_WS>")
        sys.exit(1)

    central_ip, central_port = sys.argv[2].split(":")
    ws_id = sys.argv[3]

    run_monitor(central_ip, int(central_port), ws_id)