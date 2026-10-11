import pandas as pd
import sympy as sp

puntos = [(1.5, 10.2), (2, 10.7), (2.5, 10.44), (3, 10.57)]  # (x, y)


def a_racional(valor):
    """Fracción exacta (evita errores de punto flotante)."""
    return sp.Rational(str(valor))


def Interpolacion_Lagrange(puntos):
    """Interpolación de Lagrange para cualquier cantidad de puntos (n >= 2).

    L_i(x) = Π_{j≠i} (x - x_j) / (x_i - x_j)
    P(x)   = Σ y_i * L_i(x)
    """
    if len(puntos) < 2:
        raise ValueError("Hacen falta al menos 2 puntos.")

    xs = [a_racional(p[0]) for p in puntos]
    ys = [a_racional(p[1]) for p in puntos]
    n = len(xs)

    if len(set(xs)) != n:
        raise ValueError("Hay valores de x repetidos: no se puede interpolar.")

    x = sp.Symbol("x")

    # Tabla de puntos (mismo formato que en Newton)
    tabla = pd.DataFrame(
        {
            "PTOS": list(range(n)),
            "xn": [float(v) for v in xs],
            "f(xn)": [float(v) for v in ys],
        }
    )

    # Polinomios de Lagrange L_i(x)
    L = []
    for i in range(n):
        Li = sp.Integer(1)
        for j in range(n):
            if j != i:
                Li *= (x - xs[j]) / (xs[i] - xs[j])
        L.append(sp.expand(Li))

    # Polinomio interpolante
    P = sp.expand(sum(ys[i] * L[i] for i in range(n)))

    return tabla, L, P, x, xs, ys


if __name__ == "__main__":
    t, L, P, x, xs, ys = Interpolacion_Lagrange(puntos)

    print("#" * 15)
    print(t)
    print("#" * 15)
    print("Polinomios de Lagrange:")
    for i, Li in enumerate(L):
        print(f"L{i}(x) = {Li}")
    print("#" * 15)
    print("Polinomio interpolante de Lagrange:")
    print(P)
    print(sp.N(P, 6))
    print("#" * 15)
    print("Verificación en los nodos:")
    for xi, yi in zip(xs, ys):
        valor = P.subs(x, xi)
        estado = "OK" if valor == yi else "ERROR"
        print(f"P({float(xi)}) = {float(valor)}  (esperado {float(yi)})  {estado}")
    print("#" * 15)