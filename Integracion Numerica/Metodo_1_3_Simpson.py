import pandas as pd
import scipy as sp

valores_x = [0.4, 0.6, 0.8, 1.0, 1.2, 
             1.4, 1.6, 1.8, 2.0, 
             2.2, 2.4, 2.6, 2.8]

valores_y = [5.1600, 3.6933, 3.1400, 3.0000, 3.1067, 
             3.3886, 3.8100, 4.3511, 5.0000, 
             5.7491, 6.5933, 7.5292, 8.5543]


valor_real = 8.43592905
valores_a_probar = [1, 2, 4, 8]


def metodo_simpson_1_3(a, b, n, valores_x, valores_y):
    h = (b - a) / n
    indice_a = valores_x.index(a)
    indice_b = valores_x.index(b)
    paso_indices = (indice_b - indice_a) // n 
    print(f"paso_indices: {paso_indices}")
    fa = valores_y[indice_a]
    fb = valores_y[indice_b]
    suma_impares = 0
    suma_pares = 0
    for i in range(1, n):
        idx = indice_a + i * paso_indices
        if i % 2 == 0:
            suma_pares += valores_y[idx]
        else:
            suma_impares += valores_y[idx]
    I = (h / 3) * (fa + 4 * suma_impares + 2 * suma_pares + fb)
    return I
    
columnas = ["n", "resultado", "error_absoluto", "error_relativo_porcentual"]
filas = []

#for n in valores_a_probar:
    #resultado = metodo_simpson_1_3(1.2, 2.8, n, valores_x, valores_y)
    #error_absoluto = abs(valor_real - resultado)
    #error_relativo_porcentual = (error_absoluto / valor_real) * 100
    #filas.append([n, resultado, error_absoluto, error_relativo_porcentual])

#df = pd.DataFrame(filas, columns=columnas)
#print(df)


