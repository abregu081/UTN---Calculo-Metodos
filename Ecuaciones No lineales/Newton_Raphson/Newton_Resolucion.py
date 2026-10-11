import os
import pandas as pd
import pandas
import sympy as sp

x = sp.Symbol('x')

funcion = x**15 - 1

def Newton_raphson(funcion, x0, tol):
    columnas = ['Iteracion', 'xn', 'f(xn)', 'f\'(xn)', 'xn+1', 'Tolerancia']
    df = pd.DataFrame(columns=columnas)
    iteracion = 0
    xn = x0
    fxn = funcion.subs(x, xn)
    dfxn = sp.diff(funcion, x).subs(x, xn)
    xn1 = xn - fxn / dfxn
    tolerancia = abs(xn1 - xn)
    
    while tolerancia > tol:
        iteracion += 1
        fxn = funcion.subs(x, xn)
        dfxn = sp.diff(funcion, x).subs(x, xn)
        
        if dfxn == 0:
            print("Derivada cero. No se puede continuar.")
            break
        
        xn1 = xn - fxn / dfxn
        tolerancia = abs(xn1 - xn)
        
        fila = [iteracion, xn, fxn, dfxn, xn1, tolerancia]
        df.loc[iteracion] = fila
        
        xn = xn1
        
    return df, xn1

if __name__ == "__main__":
    resultado, raiz = Newton_raphson(funcion, 0.5, 0.001)
    resultado.to_csv(os.path.join(os.path.dirname(__file__), "Newton_Raphson_Resultados.csv"), index=False)
    print(f"Raíz aproximada: {raiz}")
    print(resultado)
    
    
        
        
    

    
    