import os
import numpy as np
import sympy as sp
import pandas as pd

x = sp.Symbol('x')
funcion_sym = x**3 - 2*x**2 - 2*x + 1
f = sp.lambdify(x, funcion_sym, 'math')   # f(x) devuelve float

def regula_falsi_illinois(f, a, b, tol, max_iter=1000):
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("f(a) y f(b) deben tener signos opuestos")

    resultados = []
    p_prev = a
    lado = 0  # -1: se movió a, +1: se movió b

    for it in range(1, max_iter + 1):
        p = (a * fb - b * fa) / (fb - fa)
        fp = f(p)
        error = abs(p - p_prev)
        resultados.append([it, a, b, fa, fb, p, fp, fa * fp, error])

        if abs(fp) < tol or error < tol:
            break

        if fp * fb < 0:
            # raíz entre p y b -> a pasa a ser p
            a, fa = p, fp
            if lado == -1:
                fb /= 2        # b quedó fijo dos veces seguidas
            lado = -1
        else:
            # raíz entre a y p -> b pasa a ser p
            b, fb = p, fp
            if lado == 1:
                fa /= 2        # a quedó fijo dos veces seguidas
            lado = 1
        p_prev = p

    return pd.DataFrame(resultados, columns=[
        'Iteracion', 'a', 'b', 'fa', 'fb', 'p', 'fp', 'Signo', 'Tolerancia'])


df = regula_falsi_illinois(f, 0, 1, 0.001 )
df.to_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       'Resultados_Regular_Falsi.csv'), index=False)
print(df)