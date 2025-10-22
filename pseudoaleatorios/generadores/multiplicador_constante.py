"""Generador por multiplicador constante."""

def multiplicador_constante(seed: int, n: int, a: int = 73):
    resultados = []
    x = seed
    for _ in range(n):
        producto = x * a
        s = str(producto).zfill(8)
        medio = s[2:6]
        if len(medio) == 3:
            medio = '0' + medio
        medio_int = int(medio)
        r = medio_int / 10000
        resultados.append((x, producto, medio, r))
        x = medio_int
    return resultados
