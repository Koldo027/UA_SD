import socket
import sys
import threading
from sockets_protocol import empaquetar, desempaquetar

def escuchar_teclado():
    simular_fuga = False
    while True:
        tecla = input()
        if tecla.strip().lower() == "k":
            simular_fuga = not simular_fuga
            print(f"[ENGINE] Modo fuga/fallo cambiado a: {simular_fuga}")