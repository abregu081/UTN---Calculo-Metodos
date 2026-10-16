import sys

import pandas as pd
import sympy as sp

sys.stdout.reconfigure(encoding="utf-8")

xsym = sp.Symbol("x")


def pedir_lista(mensaje):
    while True:
        texto = input(mensaje).strip()
        try:
            valores = [float(v.strip()) for v in texto.split(",") if v.strip() != ""]
            if not valores:
                raise ValueError
            return valores
        except ValueError:
            print("  -> Valores inválidos. Ingresá números separados por comas, ej: 1, 1.5, 2, 2.5")


def a_racional(valor):
    """Pasa el número a fracción exacta (evita errores de punto flotante)."""
    return sp.Rational(str(valor))


def es_equiespaciado(xs):
    pasos = [round(xs[i + 1] - xs[i], 10) for i in range(len(xs) - 1)]
    return all(abs(p - pasos[0]) < 1e-9 for p in pasos)


# ---------------------------------------------------------------------------
# En vez de fórmulas con "h" fijo (que solo valen si los x están
# equiespaciados), para cada punto armamos el polinomio de Newton por
# diferencias divididas que pasa EXACTO por los puntos de su ventana local
# (2 o 3 puntos vecinos) y lo derivamos de forma simbólica. Esto funciona
# siempre, estén o no equiespaciados los datos; si lo están, da el mismo
# resultado que las fórmulas clásicas de diferencias finitas.
# ---------------------------------------------------------------------------

def polinomio_newton(xs_local, fs_local):
    """Polinomio que interpola exactamente los puntos (xs_local, fs_local)."""
    n = len(xs_local)
    xs_r = [a_racional(v) for v in xs_local]
    fs_r = [a_racional(v) for v in fs_local]

    diffs = [fs_r]
    for j in range(1, n):
        anterior = diffs[-1]
        diffs.append(
            [(anterior[k + 1] - anterior[k]) / (xs_r[k + j] - xs_r[k]) for k in range(n - j)]
        )

    polinomio = fs_r[0]
    producto = sp.Integer(1)
    for j in range(1, n):
        producto *= (xsym - xs_r[j - 1])
        polinomio += diffs[j][0] * producto
    return sp.expand(polinomio)


def elegir_ventana(n, i, tam):
    """Elige 'tam' índices vecinos a i: centrada si hay vecinos a ambos lados,
    si no, adelante (si i está al principio) o atrás (si i está al final)."""
    mitad = tam // 2
    inicio = max(0, i - mitad)
    inicio = min(inicio, n - tam)
    return list(range(inicio, inicio + tam))


def tipo_ventana(idxs, i):
    if idxs[0] == i:
        return "Adelante"
    if idxs[-1] == i:
        return "Atrás"
    return "Centrada"


def calcular_tabla(xs, fs, orden):
    n = len(xs)
    tam_ventana = min(3, n)
    filas = []
    for i in range(n):
        idxs = elegir_ventana(n, i, tam_ventana)
        xs_local = [xs[k] for k in idxs]
        fs_local = [fs[k] for k in idxs]

        P = polinomio_newton(xs_local, fs_local)
        deriv = sp.diff(P, xsym, orden)
        valor = float(deriv.subs(xsym, a_racional(xs[i])))

        tipo = tipo_ventana(idxs, i)
        puntos_usados = ", ".join(f"x={xs[k]:g}" for k in idxs)
        filas.append({
            "i": i,
            "x_i": xs[i],
            "f(x_i)": fs[i],
            "Puntos usados": puntos_usados,
            "Tipo": f"{tipo} (grado {tam_ventana - 1})",
            f"y^({orden})(x_i) aprox": valor,
        })
    return pd.DataFrame(filas)


def main():
    print("#" * 70)
    print("TAYLOR_TABLA: derivación numérica a partir de una tabla de puntos")
    print("(funciona con x equiespaciados o NO equiespaciados)")
    print("#" * 70)

    xs = pedir_lista("Ingresá los valores de x separados por comas: ")
    fs = pedir_lista("Ingresá los valores de f(x) separados por comas: ")

    if len(xs) != len(fs):
        print("Error: la cantidad de valores de x y de f(x) no coincide.")
        return

    n = len(xs)
    print(f"\nCargaste {n} puntos.")

    if n < 2:
        print("Hacen falta al menos 2 puntos para calcular cualquier derivada.")
        return

    if es_equiespaciado(xs):
        print("Los puntos están equiespaciados (h constante).")
    else:
        print("Los puntos NO están equiespaciados: se va a interpolar un "
              "polinomio local (Newton, diferencias divididas) para cada punto "
              "y derivarlo, en vez de usar una fórmula con h fijo.")

    print("\n¿Cuántos puntos se pueden calcular?")
    if n >= 3:
        print(
            f"- Derivada 1ra: se puede calcular en los {n} puntos "
            f"(adelante en el primero, centrada en los {n - 2} interiores, "
            f"atrás en el último; en cada caso se ajusta una parábola local "
            f"con 3 puntos y se deriva)."
        )
        print(
            f"- Derivada 2da: se puede calcular en los {n} puntos, con el "
            f"mismo criterio de ventana."
        )
    else:
        print(
            f"- Derivada 1ra: solo con la pendiente entre los 2 puntos "
            f"(recta), en los {n} puntos."
        )
        print("- Derivada 2da: no se puede calcular (hacen falta al menos 3 puntos).")

    while True:
        orden_txt = input("\n¿Querés calcular la derivada 1ra o 2da? (1/2): ").strip()
        if orden_txt in ("1", "2"):
            orden = int(orden_txt)
            break
        print("  -> Ingresá 1 o 2.")

    if orden == 2 and n < 3:
        print("No se puede calcular la derivada 2da con menos de 3 puntos.")
        return

    tabla = calcular_tabla(xs, fs, orden)
    print("\nResultado:")
    print(tabla.to_string(index=False))


if __name__ == "__main__":
    main()
