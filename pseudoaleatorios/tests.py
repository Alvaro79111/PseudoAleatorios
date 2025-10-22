"""Statistical tests for generated pseudo-random numbers.
"""
import math
from scipy.stats import norm, chi2
from typing import List, Tuple


def prueba_medias(valores: List[float], alpha: float) -> Tuple[float, float, float, bool]:
    n = len(valores)
    media = sum(valores) / n
    z0 = (media - 0.5) / (math.sqrt(1/(12*n)))
    z_alpha = norm.ppf(1 - alpha/2)
    return media, z0, z_alpha, abs(z0) < z_alpha


def prueba_varianza(valores: List[float], alpha: float) -> Tuple[float, float, float, float, bool]:
    n = len(valores)
    media = sum(valores)/n
    # varianza muestral
    var = sum((x - media)**2 for x in valores)/(n-1)
    chi_inf = chi2.ppf(alpha/2, n-1)
    chi_sup = chi2.ppf(1 - alpha/2, n-1)
    stat = (n-1)*var
    return var, stat, chi_inf, chi_sup, chi_inf <= stat <= chi_sup


def prueba_uniformidad(valores: List[float], alpha: float, k: int = 10) -> Tuple[List[int], float, float, bool]:
    n = len(valores)
    frec_obs = [0]*k
    for v in valores:
        idx = min(int(v*k), k-1)
        frec_obs[idx] += 1
    esperada = n/k
    chi_calc = sum((fo-esperada)**2/esperada for fo in frec_obs)
    chi_tabla = chi2.ppf(1-alpha, k-1)
    return frec_obs, chi_calc, chi_tabla, chi_calc < chi_tabla


def prueba_uniformidad_detallada(valores: List[float], alpha: float, k: int = 10):
    n = len(valores)
    frec_obs = [0]*k
    for v in valores:
        idx = min(int(v*k), k-1)
        frec_obs[idx] += 1
    esperada = n/k
    chi_calc = 0
    tabla = []
    for i in range(k):
        fo = frec_obs[i]
        fe = esperada
        chi = (fo-fe)**2/fe
        chi_calc += chi
        intervalo = f"[{i/k:.2f}, {(i+1)/k:.2f})"
        tabla.append((intervalo, fo, f"{fe:.2f}", f"{chi:.4f}"))
    chi_tabla = chi2.ppf(1-alpha, k-1)
    return frec_obs, chi_calc, chi_tabla, chi_calc < chi_tabla, tabla
