import pandas as pd
from random import random
from math import exp
import numpy as np
import matplotlib.pyplot as plt

desired_width = 1000
pd.set_option("display.max_columns", 12)
pd.set_option("display.max_rows", 100)
pd.set_option('display.width', desired_width)
pd.set_option('display.colheader_justify', 'left')

'''

Ejercicio Teoría de Colas:

Consideraciones:
                + El 'Si' en servicios indica que el servicio termina de realizarse en esa franja de tiempo. Esto no 
               indica el momento en que empieza a ser atendido sino el final del servicio.
                + El cliente empieza a ser atendido cuando está primero en la cola y se terminó de atender al anterior.
                + El 'Si' de llegada indica que ha ingresado a la cola.

'''

a = 0
N = 0
x = 1/10  # 0.1 hora = 6 min
landa = 3  # Por hora
mu = 5     # Por hora
t_salida = 1/mu


t = 0
ts = x*60  # 6 min
iteraciones = 1000
tiempo_total = ts*iteraciones

mu_min = mu/60
landa_min = landa/60
### Calculado:
Ws = round(1/(mu_min-landa_min))
Wq = landa_min/(mu_min*(mu_min-landa_min))
Lq = round(landa_min*Wq)
L = Lq + landa_min/mu_min
Ts = 1/mu_min
Tl = 1/landa_min


vec_tiempo = []
vec_N = []
vec_pl = []
vec_bool_llegada = []
vec_ps = []
vec_bool_salida = []

# Los tiempos transcurridos entre dos sucesos sucesivos de parámetro lambda*t siguen la distribución exponencial.
# Función de distribución exponencial acumulada:
pl = 1-exp(-landa * x)
ps = 1-exp(-mu * x)


while t < tiempo_total:

    ra = random()
    rd = random()

    if rd < ps and N != 0:
        N -= 1
        salida = 'Si'
    else:
        salida = 'No'
    if ra < pl:
        N += 1
        llegada = 'Si'
    else:
        llegada = 'No'

    t += ts

    vec_tiempo.append(t)
    vec_N.append(N)
    vec_pl.append(ra)
    vec_bool_llegada.append(llegada)
    vec_ps.append(rd)
    vec_bool_salida.append(salida)


df = pd.DataFrame({
    'tiempo(min)': vec_tiempo,
    'N(t)': vec_N,
    'Ra': vec_pl,
    '¿Llegada en el intervalo?': vec_bool_llegada,
    'Rd': vec_ps,
    '¿Salida en el intervalo?': vec_bool_salida
})
df.name = 'Datos Principales:'

print(df.name)
print(df)
print()

#################################################################################################
### Estado del Sistema:
max_mean = df['N(t)'].agg(['max', 'mean']).tolist()

print('Máximo número de personas en la cola registrado: {}'.format(max_mean[0]))
print('Promedio de personas en la cola: {}'.format(max_mean[1]))
print('Largo de la cola L esperado: {}'.format(L))
print()

##################################################################################################
### Tiempo entre llegadas ###

vector_evento_llegada = df['¿Llegada en el intervalo?'].map({'Si': 1, 'No': 0})
locl = np.where(vector_evento_llegada == 1)

for pos1 in locl:
    vec_t_llegadas = df['tiempo(min)'][pos1]
    num_llegadas = len(pos1)

tiempo_entre_llegadas = vec_t_llegadas.diff().fillna(vec_t_llegadas.iloc[0])
tiempo_medio_entre_llegadas = round(tiempo_entre_llegadas.mean(), 2)
tiempo_max_entre_llegadas = tiempo_entre_llegadas.max()
tiempo_min_entre_llegadas = tiempo_entre_llegadas.min()

print('Tiempo promedio entre llegadas: {}'.format(tiempo_medio_entre_llegadas) + ' min')
print('Máximo tiempo entre llegadas registrado: {}'.format(tiempo_max_entre_llegadas) + ' min')
print('Mínimo tiempo entre llegadas registrado: {}'.format(tiempo_min_entre_llegadas) + ' min')
print('Tiempo esperado entre llegadas 1/landa: {} min'.format(Tl))
print()

###################################################################################################
### Tiempo en el sistema ###

vector_evento_terminacion_servicio = df['¿Salida en el intervalo?'].map({'Si': 1, 'No': 0})
locs = np.where(vector_evento_terminacion_servicio == 1)

for pos2 in locs:
    vec_t_salidas = df['tiempo(min)'][pos2]
    num_servicios = len(pos2)

# Agrupo los tiempos de llegada y de servicio en dos vectores y los resto considerando que el primero que entró es será
# el primero en salir. Primer 'Si' de entrada corresponde con el primero 'Si' de salida.
tiempo_en_sistema = []
for i in range(len(vec_t_salidas)):
    tiempo_en_sistema.append(round(vec_t_salidas.iloc[i] - vec_t_llegadas.iloc[i]))

tsist_series = pd.Series(tiempo_en_sistema)
tiempo_medio_en_sistema = round(tsist_series.mean(), 2)
tiempo_en_sist_max = tsist_series.max()
tiempo_en_sist_min = tsist_series.min()

print('Tiempo promedio en el sistema: {}'.format(tiempo_medio_en_sistema) + ' min')
print('Máximo tiempo dentro del sistema registrado: {}'.format(tiempo_en_sist_max) + ' min')
print('Mínimo tiempo dentro del sistema registrado: {}'.format(tiempo_en_sist_min) + ' min')
##############
print('Tiempo de espera esperado Ws en el sistema: {} min'.format(Ws))
print()
#############################################################################################
### Tiempo desperdiciado ###

clientes_en_sistema = 0
pos3 = []
flujo_clientes_en_sistema = vector_evento_llegada - vector_evento_terminacion_servicio
for i in range(len(flujo_clientes_en_sistema)):
    if clientes_en_sistema == 0 and flujo_clientes_en_sistema[i] != 1:  # 0 clientes. No hay Trabajo
        pos3.append(i)
    clientes_en_sistema += flujo_clientes_en_sistema[i]
t_total_desperdiciado = len(pos3)*6  # Nro de períodos donde ocurre esto * 6 min: duración de c/período.
porcentaje_t_desperdiciado = round((t_total_desperdiciado / (tiempo_total)) * 100)

print('Tiempo total desperdiciado: {} hs'.format(t_total_desperdiciado/60))
print('Tiempo total: {} hs'.format(tiempo_total/60))
print('Tiempo porcentual de desperdicio: {}%'.format(porcentaje_t_desperdiciado))
print()

#############################################################################################
### Tiempo de duración del servicio ###

# Si N=1 y flujo=1 es porque antes N=0 es decir me quedo sin clientes para atender -> El siguiente to es esta iteracion
# vec_eve_term_serv[+1] = to -> cuando

# Primer pos -> E=Si
# Analizo primero pos servicio +1 -> Qué pasa con N
# N=0  -> to= pr+oximo E=1
# N!=0 -> to= siguiente pos.

to = []
tf = locs[0].tolist()  # locs: posiciones donde terminan servicios.
to.append(locl[0][0])  # locl: posiciones donde ocurren llegadas.

for i in range(len(locs[0])):
    pos1 = locs[0][i]
    if df['N(t)'][pos1] == 0:
        aux = vector_evento_llegada.tolist()[pos1:]
        ### Si aux lleno de ceros -> no hacer nada
        try:
            i = aux.index(1)
            to.append(i + pos1)  # Logro la pos original del vector entrada.
        except:
            pass
    else:
        if pos1 < len(vector_evento_terminacion_servicio) - 1:
            to.append(pos1 + 1)
if len(to) > len(tf):
    # Si hay alguien atendiendo cuando se termina el muestreo, cierro en la última pos.
    tf.append(len(vector_evento_terminacion_servicio) - 1)
vec_tf = df['tiempo(min)'][tf]
vec_to = df['tiempo(min)'][to]

vector_duracion_servicio = []
for i in range(len(to)):
    vector_duracion_servicio.append(vec_tf.iloc[i] - vec_to.iloc[i])
vec_dur_ser_series = pd.Series(vector_duracion_servicio)
duracion_promedio_del_servicio = round(vec_dur_ser_series.mean())
duracion_max_servicio = vec_dur_ser_series.max()
duracion_min_servicio = vec_dur_ser_series.min()

print('Duración promedio del servicio: {} min'.format(duracion_promedio_del_servicio))
print('Máxima duración del servicio registrada: {} min'.format(duracion_max_servicio))
print('Mínima duración del servicio registrada: {} min'.format(duracion_min_servicio))
print('Tiempo estimado de servicio 1/mu: {} min'.format(Ts))
print()


###################################################################################

df_promedios = pd.DataFrame({
    'Tiempo entre Arribos [min]': tiempo_medio_entre_llegadas,
    'Tiempo total en el sistema [min]': tiempo_medio_en_sistema,
    'Duración del servicio [min]': duracion_promedio_del_servicio,
    'Tiempo sin trabajo [%]': porcentaje_t_desperdiciado
}, index=['Resultados: '])
df_promedios.name = 'Promedios:'

# print(df_promedios.name)
# print(df_promedios)
print()


df3 = pd.DataFrame(np.array([[tiempo_medio_entre_llegadas, duracion_promedio_del_servicio,
           max_mean[1], tiempo_medio_en_sistema],
          [Tl, Ts, Lq, Ws]]).transpose(), index=['Tl', 'Ts', 'Nro_fila', 'T_sis'], columns=['Simulado', 'Calculado'])
df4 = df3.apply(np.diff, axis=1)
df4 = df4.apply(np.round)

df5 = pd.concat([df3, df4], axis=1)
df5.rename(columns={0: 'Diferencia'}, inplace=True)

print(df5)