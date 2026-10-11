import sympy as sp
import pandas as pd

x, y = sp.symbols('x y')
f_sym = sp.exp(-x) + x          # y' = f(x, y)
f = sp.lambdify((x, y), f_sym, 'math')

valor_funcion_integrada = sp.integrate(f_sym, x)

def runge_kutta_4(f, x0, y0, h, x_final):
    filas = []
    n = round((x_final - x0) / h)
    yn = y0

    for i in range(n + 1):
        xn = x0 + i * h
        k1 = h * f(xn, yn)
        k2 = h * f(xn + h/2, yn + k1/2)
        k3 = h * f(xn + h/2, yn + k2/2)
        k4 = h * f(xn + h,   yn + k3)
        yn1 = yn + (k1 + 2*k2 + 2*k3 + k4) / 6

        filas.append({
            'Iteración': i,
            'Xn': xn,
            'Yn': yn,
            'K1': k1,
            'K2': k2,
            'K3': k3,
            'K4': k4,
            'Yn+1': yn1
        })
        yn = yn1

    return pd.DataFrame(filas)

resultado = runge_kutta_4(f, x0=0, y0=0, h=0.001, x_final=1)
print(resultado)
print(valor_funcion_integrada)