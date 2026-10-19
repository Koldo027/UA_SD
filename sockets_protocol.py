STX = "\x02"
ETX = "\x03"

def calcular_lrc(cadena: str) -> str:
    lrc = 0
    for ch in cadena.encode('utf-8'):
        lrc ^= ch
    return chr(lrc)

def empaquetar(mensaje: str) -> str:
    lrc = calcular_lrc(mensaje)
    return f"{STX}{mensaje}{ETX}{lrc}"

def desempaquetar(trama: str):
    if not trama.startswith(STX) or ETX not in trama:
        return None
    try:
        fin_datos = trama.rfind(ETX)
        datos = trama[1:fin_datos]
        lrc_recibido = trama[fin_datos + 1:]
        if calcular_lrc(datos) == lrc_recibido:
            return datos
        return None
    except Exception:
        return None