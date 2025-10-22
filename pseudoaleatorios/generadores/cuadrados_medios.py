"""Generador por cuadrados medios."""

def cuadrados_medios(seed: int, n: int):
    resultados = []
    x = seed
    for _ in range(n):
        cuadrado = str(x**2).zfill(8)
        medio = cuadrado[2:6]
        if len(medio) == 3:
            medio = '0' + medio
        medio_int = int(medio)
        r = medio_int / 10000
        resultados.append((x, cuadrado, medio, r))
        x = medio_int
    return resultados
