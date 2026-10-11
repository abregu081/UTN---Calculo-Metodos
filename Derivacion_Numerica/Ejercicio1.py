import os
import sympy as sp
import pandas as pd
import math

x = sp.symbols('x')

valores_h = [0.1, 0.05, 0.025]

y = sp.sqrt(x)

def derivada_numerica_diferencia_adelante(funcion, valor_x, h):
    derivada = (funcion.subs(x, valor_x + h) - funcion.subs(x, valor_x)) / h
    return derivada.evalf()

def derivada_numerica_diferencia_atras(funcion, valor_x, h):
    derivada = (funcion.subs(x, valor_x) - funcion.subs(x, valor_x - h)) / h
    return derivada.evalf()

def derivada_numerica_diferencia_centrada(funcion, valor_x, h):
    derivada = (funcion.subs(x, valor_x + h) - funcion.subs(x, valor_x - h)) / (2 * h)
    return derivada.evalf()

filas = []
v = 1

for i in valores_h:
    r_derivada_adelante = derivada_numerica_diferencia_adelante(y, v, i)
    r_derivada_atras = derivada_numerica_diferencia_atras(y, v, i)
    r_derivada_centrada = derivada_numerica_diferencia_centrada(y, v, i)
    valor_exacto = sp.cos(v).evalf()
    diferencia_adelante = abs(r_derivada_adelante - valor_exacto)
    diferencia_atras = abs(r_derivada_atras - valor_exacto)
    diferencia_centrada = abs(r_derivada_centrada - valor_exacto)
    filas.append({
        'h': i,
        'Dx Adelante': r_derivada_adelante,
        'Dx Atrás': r_derivada_atras,
        'Dx Centrada': r_derivada_centrada,
        'Diferencia Adelante': diferencia_adelante,
        'Diferencia Atrás': diferencia_atras,
        'Diferencia Centrada': diferencia_centrada,
        'Valor exacto': valor_exacto
    })

tabla = pd.DataFrame(filas)

print(tabla)