import os
import sympy as sp
import pandas as pd

x = sp.Symbol('x')
funcion = x**5 - 3*x**2 + 3

def Regular_falsi(funcion, a, b, tol):
    iteracion = 0
    resultados = []
    contador_b = 0
    contador_a = 0
    fa_corregido = False
    fb_corregido = False
    fa = funcion.subs(x, a)
    fb = funcion.subs(x, b)
    df = pd.DataFrame(columns=['Iteracion', 'a', 'b', 'fa', 'fb', 'p', 'Signo', 'Tolerancia'])
    while abs(b - a) >= tol:
        iteracion += 1
        tolerancia = abs(b - a)
        if not fa_corregido:
            fa = funcion.subs(x, a)
        if not fb_corregido:
            fb = funcion.subs(x, b)
        fa_corregido = False
        fb_corregido = False

        p = a - ((b - a)/(fb - fa)) * fa
        fp = funcion.subs(x, p)
        signo = fa * fp
        resultados.append([iteracion, a, b, fa, fb, p, fp, signo, tolerancia])
        if signo < 0:
            b = p
            contador_a += 1
            contador_b = 0
            if contador_a == 2:
                contador_a = 0
                fa = funcion.subs(x, a)/2
                fa_corregido = True
        else:
            a = p
            contador_b += 1
            contador_a = 0
            if contador_b == 2:
                contador_b = 0
                fb = funcion.subs(x, b)/2
                fb_corregido = True
        
    df = pd.DataFrame(resultados, columns=['Iteracion', 'a', 'b', 'fa', 'fb', 'p', 'fp', 'Signo', 'Tolerancia'])
    return df

regFalsi = Regular_falsi(funcion, -1.0, 0.0, 0.0001)
regFalsi.to_csv(os.path.join(os.path.dirname(__file__), 'Resultados_Regular_Falsi.csv'), index=False)
print(regFalsi)
        
         
         
        
        