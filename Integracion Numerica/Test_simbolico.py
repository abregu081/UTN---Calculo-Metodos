import sympy as sp


x = sp.symbols('x')
f = (x**4) * sp.sqrt(4 - x**2)

a = 0
b = 2


def fmt(v, dec=6):
    """Número -> texto con pocos decimales."""
    return f"{float(v):.{dec}f}"


def metodo_simpson_1_3(f, a, b, n, desplazamiento=0):
    """
    Devuelve (valor, expresion_simbolica, expresion_numerica).
    'desplazamiento' solo cambia los nombres f_i del texto: sirve para que, cuando
    este tramo es la segunda parte de la combinada, se escriba f3, f4, ... y no f0, f1, ...
    """
    if n < 2 or n % 2 != 0:
        raise ValueError(f"Simpson 1/3 necesita n par (recibido: {n}).")
    h = (b - a) / n
    indice = [i for i in range(n + 1)]
    xi = [a + i * h for i in indice]
    fi = [f.subs(x, xi[i]) for i in indice]

    # índices de cada grupo: se usan para calcular Y para escribir
    ind_pares = [i for i in range(1, n) if i % 2 == 0]
    ind_impares = [i for i in range(1, n) if i % 2 != 0]

    valor = (h / 3) * (fi[0] + 2 * sum(fi[i] for i in ind_pares)
                       + 4 * sum(fi[i] for i in ind_impares) + fi[-1])

    # --- expresión simbólica (f0, f1, ...) ---
    d = desplazamiento
    partes = [f"f{d}", "4*(" + " + ".join(f"f{i + d}" for i in ind_impares) + ")"]
    if ind_pares:
        partes.append("2*(" + " + ".join(f"f{i + d}" for i in ind_pares) + ")")
    partes.append(f"f{n + d}")
    simbolica = f"(h/3) * ({' + '.join(partes)})"

    # --- expresión con valores reemplazados ---
    partes = [fmt(fi[0]), "4*(" + " + ".join(fmt(fi[i]) for i in ind_impares) + ")"]
    if ind_pares:
        partes.append("2*(" + " + ".join(fmt(fi[i]) for i in ind_pares) + ")")
    partes.append(fmt(fi[-1]))
    numerica = f"({fmt(h / 3)}) * ({' + '.join(partes)})"

    return float(valor), simbolica, numerica


def metodo_simpson_3_8(f, a, b, n, desplazamiento=0):
    """Devuelve (valor, expresion_simbolica, expresion_numerica)."""
    if n < 3 or n % 3 != 0:
        raise ValueError(f"Simpson 3/8 necesita n múltiplo de 3 (recibido: {n}).")
    h = (b - a) / n
    indice = [i for i in range(n + 1)]
    xi = [a + i * h for i in indice]
    fi = [f.subs(x, xi[i]) for i in indice]

    ind_mult = [i for i in range(1, n) if i % 3 == 0]
    ind_no_mult = [i for i in range(1, n) if i % 3 != 0]

    valor = (3 * h / 8) * (fi[0] + 3 * sum(fi[i] for i in ind_no_mult)
                           + 2 * sum(fi[i] for i in ind_mult) + fi[-1])

    # --- expresión simbólica ---
    d = desplazamiento
    partes = [f"f{d}", "3*(" + " + ".join(f"f{i + d}" for i in ind_no_mult) + ")"]
    if ind_mult:
        partes.append("2*(" + " + ".join(f"f{i + d}" for i in ind_mult) + ")")
    partes.append(f"f{n + d}")
    simbolica = f"(3*h/8) * ({' + '.join(partes)})"

    # --- expresión con valores reemplazados ---
    partes = [fmt(fi[0]), "3*(" + " + ".join(fmt(fi[i]) for i in ind_no_mult) + ")"]
    if ind_mult:
        partes.append("2*(" + " + ".join(fmt(fi[i]) for i in ind_mult) + ")")
    partes.append(fmt(fi[-1]))
    numerica = f"({fmt(3 * h / 8)}) * ({' + '.join(partes)})"

    return float(valor), simbolica, numerica


def simpson_combinado(f, a, b, n):
    """
    n par   -> 1/3 en todo el intervalo.
    n = 3   -> un solo bloque de 3/8.
    n impar -> 3/8 en los primeros 3 subintervalos + 1/3 en los n-3 restantes.
    Devuelve (valor, expresion_simbolica, expresion_numerica).
    """
    if isinstance(n, bool) or not isinstance(n, int) or n < 2:
        raise ValueError(f"n debe ser un entero >= 2 (recibido: {n!r}).")
    if n % 2 == 0:
        return metodo_simpson_1_3(f, a, b, n)
    if n == 3:
        return metodo_simpson_3_8(f, a, b, 3)

    h = (b - a) / n
    x3 = a + 3 * h
    v38, s38, n38 = metodo_simpson_3_8(f, a, x3, 3)
    v13, s13, n13 = metodo_simpson_1_3(f, x3, b, n - 3, desplazamiento=3)

    simbolica = f"[3/8: {s38}] + [1/3: {s13}]"
    numerica = f"[3/8: {n38}] + [1/3: {n13}]"
    return v38 + v13, simbolica, numerica


if __name__ == "__main__":
    casos = [("combinado", simpson_combinado, 11)]
    for nombre, metodo, n in casos:
        valor, simb, num = metodo(f, a, b, n)
        print(f"--- {nombre}, n = {n} ---")
        print("simbólica:", simb)
        print("numérica :", num)
        print("valor    :", valor)
        print()