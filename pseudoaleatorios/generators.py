"""Generators for pseudo-random numbers using classical algorithms.
"""
import math
from .generadores.cuadrados_medios import cuadrados_medios
from .generadores.productos_medios import productos_medios
from .generadores.multiplicador_constante import multiplicador_constante


def cuadrados_medios(seed: int, n: int):
    """Cuadrados medios: devuelve lista de tuplas (Xi, Xi^2, medio, Ri)
    """
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


def productos_medios(seedx: int, seedy: int, n: int):
    """Productos medios: devuelve lista de tuplas (Xi, Yi, Xi*Yi, medio, Ri)
    """
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


def multiplicador_constante(seed: int, n: int, a: int = 73):
    """Multiplicador constante: devuelve lista de tuplas (Xi, a*Xi, medio, Ri)
    """
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
