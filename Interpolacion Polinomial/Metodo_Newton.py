import sympy as sp
import pandas as pd
from math import factorial

valores_x = [0,1,2,3]
valores_fx = [10.39,12.61,20.72,40.74]


def a_racional(valor):
    """Pasa el número a fracción exacta (evita errores tipo 9.7 - 11 = -1.3000000000000007)."""
    return sp.Rational(str(valor))


def newton_progresivo(x_values, fx_values):
    """Interpolación de Newton progresiva (nodos equiespaciados).

    s = (x - x0) / h
    g(s) = f(x0) + s*Δf(x0) + s(s-1)/2! * Δ²f(x0) + s(s-1)(s-2)/3! * Δ³f(x0) + ...
    """
    if len(x_values) != len(fx_values):
        raise ValueError("x y f(x) tienen que tener la misma cantidad de valores.")
    if len(x_values) < 2:
        raise ValueError("Hacen falta al menos 2 puntos.")

    xs = [a_racional(v) for v in x_values]
    fs = [a_racional(v) for v in fx_values]
    n = len(xs)

    # Paso h y verificación de nodos equiespaciados
    h = xs[1] - xs[0]
    if h <= 0:
        raise ValueError("Los valores de x deben estar en orden creciente.")
    for i in range(1, n):
        if xs[i] - xs[i - 1] != h:
            raise ValueError("Los nodos no son equiespaciados: esta fórmula no se puede usar.")

    # diffs[j][i] = diferencia progresiva de orden j que empieza en la fila i
    diffs = [fs]
    for _ in range(1, n):
        anterior = diffs[-1]
        diffs.append([anterior[i + 1] - anterior[i] for i in range(len(anterior) - 1)])

    # Tabla (s = (xi - x0)/h, o sea 0, 1, 2, ...)
    encabezado = ["s", "xn", "f(xn)"] + [f"Δ{j}f" for j in range(1, n)]
    filas = []
    for i in range(n):
        fila = {
            "s": float((xs[i] - xs[0]) / h),
            "xn": float(xs[i]),
            "f(xn)": float(fs[i]),
        }
        for j in range(1, n):
            fila[f"Δ{j}f"] = float(diffs[j][i]) if i < len(diffs[j]) else None
        filas.append(fila)
    tabla = pd.DataFrame(filas, columns=encabezado)

    # Polinomio: los coeficientes son los de la PRIMERA fila de la tabla
    x = sp.Symbol("x")
    s = (x - xs[0]) / h
    formula = fs[0]
    for j in range(1, n):
        termino = diffs[j][0]
        for k in range(j):
            termino *= (s - k)
        formula += termino / factorial(j)

    return tabla, sp.expand(formula), x, xs, fs


if __name__ == "__main__":
    t, formula, x, xs, fs = newton_progresivo(valores_x, valores_fx)

    print("#" * 15)
    print(t)
    print("#" * 15)
    print("Fórmula de interpolación de Newton:")
    print(formula)
    print(sp.N(formula, 6))
    print("#" * 15)
    print("Verificación en los nodos:")
    for xi, fi in zip(xs, fs):
        valor = formula.subs(x, xi)
        estado = "OK" if valor == fi else "ERROR"
        print(f"P({float(xi)}) = {float(valor)}  (esperado {float(fi)})  {estado}")
    print("#" * 15)