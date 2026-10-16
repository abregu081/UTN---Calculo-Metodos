import os
import sympy as sp


x = sp.symbols('x')
f = (x**4) * sp.sqrt(4- x**2)

a = 0
b = 2


def metodo_simpson_1_3(f, a, b, n):
    h = (b - a) / n
    indice = [i for i in range(n + 1)]
    xi = [a + i * h for i in indice]
    fi = [f.subs(x, xi[i]) for i in indice]
    pares = [fi[i] for i in range(1, n) if i % 2 == 0]
    impares = [fi[i] for i in range(1, n) if i % 2 != 0]
    valor = (h / 3) * (fi[0] + 2 * sum(pares) + 4 * sum(impares) + fi[-1])
    return valor

def metodo_simpson_3_8(f, a, b, n):
    h = (b - a) / n
    indice = [i for i in range(n + 1)]
    xi = [a + i * h for i in indice]
    fi = [f.subs(x, xi[i]) for i in indice]
    multiplos_de_tres = [fi[i] for i in range(1, n) if i % 3 == 0]
    no_multiplos_de_tres = [fi[i] for i in range(1, n) if i % 3 != 0]
    valor = (3 * h / 8) * (fi[0] + 3 * sum(no_multiplos_de_tres) + 2 * sum(multiplos_de_tres) + fi[-1])
    return valor

def simpson_combinado(f, a, b, n):
    if n % 2 == 0:
        return metodo_simpson_1_3(f, a, b, n)
    h = (b - a) / n
    x3 = a + 3 * h
    return metodo_simpson_3_8(f, a, x3, 3) + metodo_simpson_1_3(f, x3, b, n - 3)


resultado = simpson_combinado(f, a, b, 11)
print(resultado)