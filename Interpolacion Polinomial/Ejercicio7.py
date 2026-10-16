import sys

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

sys.stdout.reconfigure(encoding="utf-8")

from Metodo_Newton_no_Informe import newton_no_uniforme

# -----------------------------------------------------------------
# Datos del punto 7
# -----------------------------------------------------------------
valores_x = [1, 2.5, 3.5, 5]
valores_fx = [1, 2, 2.8, 3.5]

print("#" * 70)
print("PASO 0: ¿Qué método corresponde?")
print("#" * 70)
print("Nodos x:", valores_x)
diffs_h = [valores_x[i + 1] - valores_x[i] for i in range(len(valores_x) - 1)]
print("Separaciones entre nodos consecutivos (h_i = x_i+1 - x_i):", diffs_h)
print(
    "Como las separaciones NO son todas iguales (1.5, 1, 1.5), los nodos son "
    "no equiespaciados. Por eso usamos 'Metodo_Newton_no_Informe.py' "
    "(diferencias divididas), que es el que sirve para separación no uniforme, "
    "y NO 'Metodo_Newton.py' (que exige h constante)."
)

# -----------------------------------------------------------------
# a) Polinomio de interpolación de grado 3
# -----------------------------------------------------------------
print()
print("#" * 70)
print("a) Polinomio de interpolación de grado 3 en (1;5)")
print("#" * 70)
print(
    "Con 4 puntos (x0,x1,x2,x3) se arma un polinomio de grado <= 3 que pasa "
    "exactamente por los 4. El método usa diferencias divididas:\n"
    "  Δ¹f[i] = (f[i+1]-f[i]) / (x[i+1]-x[i])\n"
    "  Δʲf[i] = (Δʲ⁻¹f[i+1]-Δʲ⁻¹f[i]) / (x[i+j]-x[i])\n"
    "y arma el polinomio tomando SIEMPRE los valores de la primera fila de la "
    "tabla (los que arrancan en x0):\n"
    "  P(x) = f(x0) + Δf[0]*(x-x0) + Δ²f[0]*(x-x0)(x-x1) + Δ³f[0]*(x-x0)(x-x1)(x-x2)"
)

tabla, P, x, xs, fs = newton_no_uniforme(valores_x, valores_fx)

print()
print("Tabla de diferencias divididas:")
print(tabla)

print()
print("Coeficientes que se usan (primera fila de la tabla):")
print(f"  f(x0)  = {tabla.iloc[0]['fx(xn)']}")
print(f"  Δ¹f[0] = {tabla.iloc[0]['Δf']}")
print(f"  Δ²f[0] = {tabla.iloc[0]['Δ²f']}")
print(f"  Δ³f[0] = {tabla.iloc[0]['Δ³f']}")

print()
print("Polinomio P(x) expandido:")
print("P(x) =", P)
print("P(x) (coeficientes numéricos) =", sp.N(P, 8))

# -----------------------------------------------------------------
# b) Gráfico de los puntos y el polinomio en (1,5)
# -----------------------------------------------------------------
print()
print("#" * 70)
print("b) Gráfico de los puntos dados y el polinomio de interpolación")
print("#" * 70)
print(
    "Graficamos los 4 puntos de la tabla (la 'función' dada son solo esos "
    "puntos) junto con la curva continua de P(x) evaluada en el intervalo [1,5]."
)

P_func = sp.lambdify(x, P, "numpy")
xs_plot = np.linspace(1, 5, 400)
ys_plot = P_func(xs_plot)

plt.figure(figsize=(8, 5))
plt.plot(xs_plot, ys_plot, label="P(x) - polinomio interpolador", color="tab:blue")
plt.scatter(valores_x, valores_fx, color="tab:red", zorder=5, label="Puntos dados (x, f(x))")
plt.title("Interpolación de Newton (diferencias divididas) - grado 3")
plt.xlabel("x")
plt.ylabel("f(x) / P(x)")
plt.grid(True, alpha=0.3)
plt.legend()
grafico_path = "Punto7_grafico.png"
plt.savefig(grafico_path, dpi=150, bbox_inches="tight")
print(f"Gráfico guardado en: {grafico_path}")

# -----------------------------------------------------------------
# c) Interpolar el valor para x = 3
# -----------------------------------------------------------------
print()
print("#" * 70)
print("c) Interpolar el valor para x = 3")
print("#" * 70)
print("Evaluamos el polinomio P(x) en x=3 (reemplazo directo en la fórmula):")
punto = sp.Integer(3)
P_3 = P.subs(x, punto)
print(f"P(3) = {sp.N(P_3, 8)}")

# -----------------------------------------------------------------
# d) Derivada aproximada en x = 3
# -----------------------------------------------------------------
print()
print("#" * 70)
print("d) Aproximar la derivada en x = 3 usando el polinomio")
print("#" * 70)
print(
    "Como P(x) es un polinomio, derivamos término a término (regla de la "
    "potencia) y evaluamos la derivada en x=3."
)
P_prima = sp.diff(P, x)
dP_3 = P_prima.subs(x, punto)
print("P'(x) =", sp.expand(P_prima))
print(f"P'(3) = {sp.N(dP_3, 8)}")

# -----------------------------------------------------------------
# e) Integral aproximada en [1, 5]
# -----------------------------------------------------------------
print()
print("#" * 70)
print("e) Aproximar la integral de la función en [1, 5] usando el polinomio")
print("#" * 70)
print(
    "Como P(x) es un polinomio, su primitiva se calcula término a término "
    "(regla de la potencia inversa) y evaluamos F(5) - F(1)."
)
integral_P = sp.integrate(P, (x, sp.Integer(1), sp.Integer(5)))
print(f"∫P(x)dx en [1,5] = {sp.N(integral_P, 8)}")

print()
print("#" * 70)
print("RESUMEN")
print("#" * 70)
print(f"P(3)        = {sp.N(P_3, 8)}")
print(f"P'(3)       = {sp.N(dP_3, 8)}")
print(f"∫[1,5]P(x)dx = {sp.N(integral_P, 8)}")
