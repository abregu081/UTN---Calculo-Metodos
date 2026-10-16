import os
import pandas as pd
import sympy as sp
import math

x = sp.Symbol('x')

funcion = sp.exp(x) - 3*x -2

def cantidad_de_iteraciones(a, b, tol):
    numerador = sp.log((b - a) / tol)
    denominador = sp.log(2)
    resultado = numerador / denominador
    n = sp.ceiling(resultado)  
    return n

def biseccion(funcion, a, b, tol):
    resultados = []
    fa = funcion.subs(x, a)
    fb = funcion.subs(x, b)
    if fa == 0:
        print(f"x={a} ya es raíz exacta (f(a)=0)")
        return pd.DataFrame([[0, a, b, fa, fb, a, 0, 0]],
                             columns=['Iteracion', 'a', 'b', 'fa', 'fb', 'Xm', 'f(a)*f(xm)', 'Tolerancia'])
    if fb == 0:
        print(f"x={b} ya es raíz exacta (f(b)=0)")
        return pd.DataFrame([[0, a, b, fa, fb, b, 0, 0]],
                             columns=['Iteracion', 'a', 'b', 'fa', 'fb', 'Xm', 'f(a)*f(xm)', 'Tolerancia'])

    if fa * fb > 0:
        print("No se puede resolver por bisección: no hay cambio de signo")
        return pd.DataFrame(columns=['Iteracion', 'a', 'b', 'fa', 'fb', 'Xm', 'f(a)*f(xm)', 'Tolerancia'])

    n = cantidad_de_iteraciones(a, b, tol)
    print("-"*5 + "Resolucion por biseccion" + "-"*5)
    print("-"*5 + f"Numero de Iteraciones calculadas = {n}" + "-"*5)

    for i in range(n):
        fa = funcion.subs(x, a)
        fb = funcion.subs(x, b)
        xm = (a + b) / 2
        fxm = funcion.subs(x, xm)

        if fxm == 0:
            resultados.append([i + 1, a, b, fa, fb, xm, fa * fxm, abs(b - a)])
            print(f"Raíz exacta encontrada en x={xm}")
            break

        if fa * fxm < 0:
            b = xm
        else:
            a = xm
        tolerancia_actual = abs(b - a)
        resultados.append([i + 1, a, b, fa, fb, xm, fa * fxm, tolerancia_actual])
        if tolerancia_actual < tol:
            print(f"Convergencia alcanzada en la iteración {i + 1}")
            break
    df = pd.DataFrame(resultados, columns=['Iteracion', 'a', 'b', 'fa', 'fb', 'Xm', 'f(a)*f(xm)', 'Tolerancia'])
    return df
biseccion_resultado = biseccion(funcion, -1, 0, 0.0001)
biseccion_resultado.to_csv(os.path.join(os.path.dirname(__file__), 'Biseccion_Resultado.csv'), index=False)
print(biseccion_resultado)

    
    
     

