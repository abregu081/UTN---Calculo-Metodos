import sympy as sp
import pandas as pd


x = sp.symbols('x')

funcion_derivada = 2 - 2*x + 4 * x**2 - 4*x**3 

f0 = 1

h = 0.1

def metodo_euler(funcion, h, f0):
    columnas = ["ITERACION", "xn", "Yn", "F(xn;Yn)", "Yn+1"]
    filas = []
    xn = 0
    Yn = f0
    iteracion = 0
    while xn <= 1:
        Fxy = funcion.subs(x, xn).subs('y', Yn)
        Yn1 = Yn + h * Fxy
        filas.append({
            "ITERACION": iteracion,
            "xn": xn,
            "Yn": Yn,
            "F(xn;Yn)": Fxy,
            "Yn+1": Yn1
        })
        iteracion += 1
        xn += h
        Yn = Yn1
    
    return pd.DataFrame(filas, columns=columnas)


def solucion_exacta(funcion):
    # como f solo depende de x, y'(x)=f(x) se integra directamente
    primitiva = sp.integrate(funcion, x)
    constante = f0 - primitiva.subs(x, 0)
    return primitiva + constante


resultado = metodo_euler(funcion_derivada, h, f0)

y_exacta = solucion_exacta(funcion_derivada)
resultado["Y exacta"] = resultado["xn"].apply(lambda xi: float(y_exacta.subs(x, xi)))
resultado["Error"] = (resultado["Y exacta"] - resultado["Yn"]).abs()

print(resultado)
print(f"\nSolucion exacta: y(x) = {y_exacta}")
