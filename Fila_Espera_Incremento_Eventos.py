import pandas as pd
from random import random
from math import exp
import numpy as np
import matplotlib.pyplot as plt



''' Generacion de observaciones aleatorias a partir de una distribución de probabilidad

Método de Transformación Inversa:

Sea F(x)=P{X <= x}

1. Se debe generar un número aleatorio uniforme r entre 0 y 1
2. Establecer F(x)=r y despejar x, que es entonces la observación aleatoria deseada que sigue la distribución
   de probabilidad dada. 
   
   Exponencial:
   
   F(x) = 1-exp(-alpha * x) = r
        x = ln( 1 - r ) / (-alpha)
        
        r y (1-r) son dos números aleatorios uniformes por lo que es una práctica común usar:
        
        x = ln(r)/(-alpha)

Este método se puede utilizar para otras distribuciones como Earlang, normal, ji cuadrada, etc.
Luego también hay otros métodos como el método de aceptación-rechazo donde la construcción de F(x)^-1 
no se puede realizar
'''

def get_intervalos(landa, mu, iteraciones):

    rl = [random() for i in range(iteraciones)]
    rs = [random() for x in range(iteraciones)]

    xl = [round(np.log(1 - r) / (-landa), 2) for r in rl]  # observación aleatoria, tiempo entre llegada
    xs = [round(np.log(1 - r) / (-mu), 2) for r in rs]  # observación aleatoria, tiempo entre servicios.

    return xl, xs


def get_timer_llegadas(delta_t):
    sum_time = 0
    timer_llegadas = []
    for time in delta_t:
        sum_time = round(sum_time + time, 2)
        timer_llegadas.append(sum_time)
    return timer_llegadas


def get_timer_servicios(delta_t, timer_llegadas):

    sum_s = [round(delta_t[0] + timer_llegadas[0], 2)]      # Primer caso
    delta_t.remove(delta_t[0])  # Para no contar el primer tiempo de nuevo.

    for z, incremento in enumerate(delta_t):

        if timer_llegadas[z + 1] > sum_s[z]:  # Si la siguiente llegada ocurre luego del siguiente servicio.
            _aux = [valor for valor in timer_llegadas if valor > sum_s[z]]  # Me quedo con los tiempos mayores a este.
            time = _aux[0]
            sum_s.append(
                round(incremento + time, 2))  # El siguiente servicio empieza desde la llegada del único cliente
        else:
            sum_s.append(
                round(incremento + sum_s[z], 2))  # El siguiente servicio empieza a contar desde el último servicio
    return sum_s


def get_states(llegadas, servicios):
    # Le cargo un parámetro para poder identificarlo
    clock = llegadas + servicios
    clock.sort()

    timer_llegadas = [(llegada, 'llegada') for llegada in llegadas]
    timer_servicios = [(servicio, 'servicio') for servicio in servicios]

    # Junto ambos timers y ordeno de menor a mayor.
    timer_general = timer_llegadas + timer_servicios
    timer_general.sort()

    # Según los timers llenaré el vector estado con el Nro de clientes en sistema.
    # Si ocurre llegada incrementa en 1, si ocurre servicio decrementa en 1.
    N_list = []
    N = 0
    for time, event in timer_general:
        if event == 'llegada':
            N = N + 1
        elif event == 'servicio':
            N = N - 1
        else:
            assert event == 'llegada' or event == 'servicio', 'Revisar código'
            print('Error')
            break
        N_list.append(N)
    return N_list, clock

def print_states_in_time(timer_llegadas, timer_servicios, estados, clock):
    time = np.arange(start=0, stop=max(timer_servicios[-1], timer_llegadas[-1]) + 0.01, step=0.01)
    time = time.round(decimals=2)  # Problema con arange que devuelve números como por ejemplo 0.100000003.

    ## Según el valor de timers llenar con el estado -> El resto NaN para poder completar con ffill
    asd = np.empty(len(time))
    asd[:] = np.nan
    asd[0] = 0

    for timer, estado in zip(clock, estados):
        aux = np.where(time == timer)[0][0]
        asd[aux] = estado

    df = pd.DataFrame(asd, index=time, columns=['Nro Clientes'])
    df.index.name = 'Tiempo [min]'
    df.fillna(method='ffill', inplace=True)

    df.plot()
    plt.show()


def get_data_frame(estados, clock):
    flujo = pd.Series(np.diff(estados))
    flujo = flujo.map({1: 'llegada', -1: 'servicio'})
    flujo = flujo.tolist()
    flujo.insert(0, 'llegada')

    dic = {
        'Nro Clientes en Sistema': estados,
        'Evento': flujo}

    df = pd.DataFrame(dic, index=clock)
    df.index.name = 'Tiempo [min]'

    return df


if __name__ == '__main__':

    # Parámetros:
    landa = 3 / 60  # por min
    mu = 5 / 60     # por min
    iteraciones = 10

    # Vectores de estado:

    delta_t_llegadas, delta_t_servicios = get_intervalos(landa, mu, iteraciones)

    timer_llegadas = get_timer_llegadas(delta_t_llegadas)

    timer_servicios = get_timer_servicios(delta_t_servicios, timer_llegadas)

    estados, clock = get_states(timer_llegadas, timer_servicios)

    df = get_data_frame(estados, clock)

   # print_states_in_time(timer_llegadas, timer_servicios, estados, clock)

    tiempo_medio_entre_llegadas = round(pd.Series(delta_t_llegadas).mean(), 2)
    tiempo_medio_duracion_servicio = round(pd.Series(delta_t_servicios).mean(), 2)




    print(df)







