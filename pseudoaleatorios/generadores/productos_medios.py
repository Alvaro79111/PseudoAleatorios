"""Generador por productos medios."""

def productos_medios(seedx: int, seedy: int, n: int):
    resultados = []
    x = seedx
    y = seedy
    for _ in range(n):
        producto = str(x * y).zfill(8)
        medio = producto[2:6]
        if len(medio) == 3:
            medio = '0' + medio
        medio_int = int(medio)
        r = medio_int / 10000
        resultados.append((x, y, producto, medio, r))
        x, y = y, medio_int
    return resultados
