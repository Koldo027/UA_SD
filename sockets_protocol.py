def calcular_lrc(cadena: str) -> str:
    lrc = 0
    for ch in cadena.encode('utf-8'):
        lrc ^= ch
    return chr(lrc)
