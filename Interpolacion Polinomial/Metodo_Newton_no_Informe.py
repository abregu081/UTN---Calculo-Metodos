import pandas as pd
import sympy as sp

valores_x = [1, 2.5, 3.5, 5]
valores_fx = [1, 2, 2.8, 3.5]

SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def a_racional(valor):
    """Fracción exacta (evita errores de punto flotante)."""
    return sp.Rational(str(valor))


def nombre_diff(j):
    return "Δf" if j == 1 else f"Δ{str(j).translate(SUP)}f"


def newton_no_uniforme(x_values, fx_values):
    """Interpolación de Newton con diferencias divididas (separación NO uniforme).

    Δ¹f[i]   = (f[i+1] - f[i]) / (x[i+1] - x[i])
    Δʲf[i]   = (Δʲ⁻¹f[i+1] - Δʲ⁻¹f[i]) / (x[i+j] - x[i])

    p(x) = f(x0) + Δf(x-x0) + Δ²f(x-x0)(x-x1) + Δ³f(x-x0)(x-x1)(x-x2) + ...
    (los coeficientes son los de la PRIMERA fila de la tabla)
    """
    if len(x_values) != len(fx_values):
        raise ValueError("x y f(x) tienen que tener la misma cantidad de valores.")
    if len(x_values) < 2:
        raise ValueError("Hacen falta al menos 2 puntos.")

    xs = [a_racional(v) for v in x_values]
    fs = [a_racional(v) for v in fx_values]
    n = len(xs)

    if len(set(xs)) != n:
        raise ValueError("Hay valores de x repetidos: no se puede interpolar.")

    # diffs[j][i] = diferencia dividida de orden j que empieza en la fila i
    diffs = [fs]
    for j in range(1, n):
        anterior = diffs[-1]
        diffs.append(
            [(anterior[i + 1] - anterior[i]) / (xs[i + j] - xs[i]) for i in range(n - j)]
        )

    # Tabla
    columnas = ["PTOS", "xn", "fx(xn)"] + [nombre_diff(j) for j in range(1, n)]
    filas = []
    for i in range(n):
        fila = {"PTOS": i, "xn": float(xs[i]), "fx(xn)": float(fs[i])}
        for j in range(1, n):
            fila[nombre_diff(j)] = float(diffs[j][i]) if i < len(diffs[j]) else None
        filas.append(fila)
    tabla = pd.DataFrame(filas, columns=columnas)

    # Polinomio de Newton
    x = sp.Symbol("x")
    formula = fs[0]
    producto = sp.Integer(1)
    for j in range(1, n):
        producto *= (x - xs[j - 1])
        formula += diffs[j][0] * producto

    return tabla, sp.expand(formula), x, xs, fs


if __name__ == "__main__":
    t, formula, x, xs, fs = newton_no_uniforme(valores_x, valores_fx)

    print("#" * 15)
    print(t)
    print("#" * 15)
    print("Fórmula de interpolación de Newton (diferencias divididas):")
    print(formula)
    print(sp.N(formula, 6))
    print("#" * 15)
    print("Verificación en los nodos:")
    for xi, fi in zip(xs, fs):
        valor = formula.subs(x, xi)
        estado = "OK" if valor == fi else "ERROR"
        print(f"P({float(xi)}) = {float(valor)}  (esperado {float(fi)})  {estado}")
    print("#" * 15)