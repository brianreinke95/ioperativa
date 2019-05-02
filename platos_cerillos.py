import pandas as pd
import numpy as np
from random import randint as rnd
import matplotlib.pyplot as plt


######################  Configuración de visualización en consola  ###################
desired_width = 1500
pd.set_option("display.max_columns", 20)
pd.set_option('display.width', desired_width)
pd.set_option('display.colheader_justify', 'left')
#####################################################################################
iteraciones = 1000

platos = [1, 2, 3, 4, 5]
loop = 0
juego_nro = []
dados_matrix = []
flujo_matrix = []
dev_matrix = []
estado_matrix = []

dev_acumulada = []
puntaje = [0] * len(platos)

while loop < iteraciones:
    dados = [rnd(1, 6) for i in range(0, len(platos))]
    # Inicializo en 0 para no tener que usar las funciones de listas.
    flujo = [0] * len(platos)
    cerillos = [0 for i in range(0, len(platos))]


    for i in range(0, len(platos)):
        if i == 0:
            flujo[i] = dados[i]
        else:
            flujo[i] = dados[i] if flujo[i-1] >= dados[i] else cerillos[i-1]
            cerillos[i-1] = max(cerillos[i - 1] - dados[i], 0)

        cerillos[i] = flujo[i] + cerillos[i]

    dev = [flujo[x] - 3.5 for x in range(0, len(platos))]

    for i in range(0, len(dev)):
        puntaje[i] += dev[i]
    print(dev)
    print(puntaje)

    dev_acumulada.append(puntaje.copy())
    entrada = dados[0]
    salida = cerillos[-1]



    dados_matrix.append(dados)
    flujo_matrix.append(flujo)
    dev_matrix.append(dev)
    estado_matrix.append(cerillos)

    juego_nro.append(loop)
    loop += 1

###############  Parámetros para definir el Multinivel  ######################

columns = ['Número de dado', 'Flujo', 'Desviacion', 'Estado']  # Primer Nivel
lon = []
for x in range(0, len(columns)):
    z = [x for i in range(0, len(juego_nro))]
    lon.extend(z)

aux = []
z = [juego_nro for i in range(0, len(columns))]
for item in z:
    aux.extend(item)

midx = pd.MultiIndex(levels=[columns, juego_nro], labels=[lon, aux], names=['', 'juego'])

####################################################################################################
#### Ordenando los vectores para lograr una matriz que concuerde con el formato del dataframe  #####

n = np.array(dados_matrix)
n2 = np.array(flujo_matrix)
n3 = np.array(dev_matrix)
n4 = np.array(estado_matrix)
n = n.transpose()
n2 = n2.transpose()
n3 = n3.transpose()
n4 = n4.transpose()

A = np.concatenate((n, n2, n3, n4), axis=1)   # Matriz de (5, n) para el dataframe.

df2 = pd.DataFrame(A, columns=midx)
df2.index.names = ['Plato']
df_por_plato = df2.stack(level=0)

print(df_por_plato)


log_df = pd.DataFrame(dev_acumulada, columns=['plato %i' % (x + 1) for x in range(0, len(platos))])
print(log_df)
plt.plot(log_df)
plt.show()

print(log_df.mean())