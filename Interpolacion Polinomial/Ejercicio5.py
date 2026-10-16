import sys

import sympy as sp

sys.stdout.reconfigure(encoding="utf-8")

from Metodo_Newton import newton_progresivo

# f(x) = 3*sqrt(3x+12) + x^3
x = sp.Symbol("x")
f_expr = 3 * sp.sqrt(3 * x + 12) + x**3
f = sp.lambdify(x, f_expr, "sympy")

# a) Nodos equiespaciados en (0,3) para un polinomio de grado 3 -> 4 puntos
valores_x = [0, 1, 2, 3]
valores_fx = [f_expr.subs(x, xi) for xi in valores_x]

tabla, P, xs_symbol, xs, fs = newton_progresivo(valores_x, [float(v) for v in valores_fx])

print("#" * 60)
print("a) Tabla de diferencias progresivas y polinomio de grado 3")
print("#" * 60)
print(tabla)
print()
print("P(x) =", P)
print("P(x) (numérico) =", sp.N(P, 8))

# b) Valor aproximado de f(1.3)
punto = sp.Rational("1.3")
P_1_3 = P.subs(xs_symbol, punto)
f_1_3_exacto = f_expr.subs(x, punto)
print()
print("#" * 60)
print("b) Aproximación de f(1.3) con el polinomio")
print("#" * 60)
print("P(1.3)        =", sp.N(P_1_3, 8))
print("f(1.3) exacto =", sp.N(f_1_3_exacto, 8))

# c) Derivada aproximada en x=1.3 usando el polinomio
P_prima = sp.diff(P, xs_symbol)
dP_1_3 = P_prima.subs(xs_symbol, punto)
f_prima_expr = sp.diff(f_expr, x)
df_1_3_exacto = f_prima_expr.subs(x, punto)
print()
print("#" * 60)
print("c) Derivada aproximada en x=1.3")
print("#" * 60)
print("P'(x)          =", sp.expand(P_prima))
print("P'(1.3)        =", sp.N(dP_1_3, 8))
print("f'(1.3) exacto =", sp.N(df_1_3_exacto, 8))

# d) Integral aproximada en [0, 2.5]
a_int, b_int = sp.Integer(0), sp.Rational("2.5")
integral_P = sp.integrate(P, (xs_symbol, a_int, b_int))
integral_f_exacta = sp.integrate(f_expr, (x, a_int, b_int))
print()
print("#" * 60)
print("d) Integral aproximada en [0, 2.5]")
print("#" * 60)
print("∫P(x)dx en [0,2.5] =", sp.N(integral_P, 8))
print("∫f(x)dx en [0,2.5] =", sp.N(integral_f_exacta, 8))

# e) Comparación de resultados (error absoluto y relativo)
print()
print("#" * 60)
print("e) Comparación con los resultados exactos")
print("#" * 60)


def comparar(nombre, aprox, exacto):
    aprox_f = float(sp.N(aprox, 12))
    exacto_f = float(sp.N(exacto, 12))
    error_abs = abs(exacto_f - aprox_f)
    error_rel = error_abs / abs(exacto_f) * 100 if exacto_f != 0 else float("nan")
    print(f"{nombre}: aprox = {aprox_f:.8f} | exacto = {exacto_f:.8f} | "
          f"error abs = {error_abs:.8f} | error rel = {error_rel:.6f}%")


comparar("f(1.3)", P_1_3, f_1_3_exacto)
comparar("f'(1.3)", dP_1_3, df_1_3_exacto)
comparar("Integral [0,2.5]", integral_P, integral_f_exacta)
