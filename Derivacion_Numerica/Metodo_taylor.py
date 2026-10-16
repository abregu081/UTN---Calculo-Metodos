import os
import sympy as sp
import pandas as pd
import math

x = sp.symbols('x')

valores_h = [0.1,0.05,0.025]

y = sp.sqrt(x)
derivada = sp.diff(y, x)
derivada_segundo_orden = sp.diff(y, x, 2)
filas = []
v = 1 # Punto en que se va a evaluar la derivada


def derivada_numerica_diferencia_adelante(funcion, valor_x, h):
    derivada = (funcion.subs(x, valor_x + h) - funcion.subs(x, valor_x)) / h
    return derivada.evalf()

def derivada_numerica_diferencia_atras(funcion, valor_x, h):
    derivada = (funcion.subs(x, valor_x) - funcion.subs(x, valor_x - h)) / h
    return derivada.evalf()

def derivada_numerica_diferencia_centrada(funcion, valor_x, h):
    derivada = (funcion.subs(x, valor_x + h) - funcion.subs(x, valor_x - h)) / (2 * h)
    return derivada.evalf()

def derivada_numerica_segundo_orden_adelante(funcion, valor_x, h):
    derivada = (funcion.subs(x,valor_x) - 2* funcion.subs(x,valor_x + h) + funcion.subs(x,valor_x + 2*h)) / (h**2)
    return derivada.evalf()

def derivada_numerica_segundo_orden_atras(funcion, valor_x, h):
    derivada = (funcion.subs(x,valor_x) - 2 * funcion.subs(x,valor_x - h) + funcion.subs(x,valor_x - 2*h)) / (h**2)
    return derivada.evalf()

def derivada_numerica_segundo_orden_centrada(funcion, valor_x, h):
    derivada = (funcion.subs(x,valor_x + h) - 2 * funcion.subs(x,valor_x) + funcion.subs(x,valor_x - h)) / (h**2)
    return derivada.evalf()



for i in valores_h:
    r_derivada_adelante = derivada_numerica_diferencia_adelante(y, v, i)
    r_derivada_atras = derivada_numerica_diferencia_atras(y, v, i)
    r_derivada_centrada = derivada_numerica_diferencia_centrada(y, v, i)
    valor_exacto = sp.diff(y, x).subs(x, v).evalf()
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

