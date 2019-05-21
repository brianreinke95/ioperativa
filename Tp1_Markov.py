import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

desired_width = 1000
pd.set_option("display.max_columns", 12)
pd.set_option("display.max_rows", 100)
pd.set_option('display.width', desired_width)
pd.set_option('display.colheader_justify', 'left')




def get_matriz_transicion(To, x_pasos):
    # Creo una nueva variable dentro de la función para que los resultados de las anteriores no me modiquen los
    # siguientes.

    T = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]  # Matriz identidad para que la primera multiplicación matricial me de T1
    for i in range(0, x_pasos):     # T3 = T1*T1*T1
        T = np.dot(T, To)
    return T

def graficar(mx):
    fig, ax = plt.subplots()
    im = ax.imshow(mx.transpose())
    # Loop over data dimensions and create text annotations.
    for i in range(6):
        for j in range(3):
            text = ax.text(i, j, mx[i, j],
                           ha="center", va="center", color="w")

    ax.set_title("Cantidad de clientes por marca por mes")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Marca")

    ylabels = (None, 'A', None, 'B', None, 'C', None)
    xlabels = (None, 0, 3, 5, 7, 9, 20)
    ax.set_xticklabels(xlabels)
    ax.set_yticklabels(ylabels)

    fig.set_size_inches(8, 5)
    plt.show()


if __name__ == '__main__':

    T = np.array([[0.3, 0.5, 0.2], [0.2, 0.6, 0.2], [0.25, 0.25, 0.5]])

    clientes_iniciales = np.array([1500, 4000, 2950])
    total_clientes = sum(clientes_iniciales)
    po = clientes_iniciales / total_clientes

    ### T 3 5 7 9 y 20:

    T3 = get_matriz_transicion(T, 3)
    T5 = get_matriz_transicion(T, 5)
    T7 = get_matriz_transicion(T, 7)
    T9 = get_matriz_transicion(T, 9)
    T20 = get_matriz_transicion(T, 20)

    p3 = np.dot(po, T3)
    p5 = np.dot(po, T5)
    p7 = np.dot(po, T7)
    p9 = np.dot(po, T9)
    p20 = np.dot(po, T20)


    clientes_3_meses = p3 * total_clientes
    clientes_5_meses = p5 * total_clientes
    clientes_7_meses = p7 * total_clientes
    clientes_9_meses = p9 * total_clientes
    clientes_20_meses = p20 * total_clientes

    clientes_3_meses = np.round(clientes_3_meses, 0)
    clientes_5_meses = np.round(clientes_5_meses, 0)
    clientes_7_meses = np.round(clientes_7_meses, 0)
    clientes_9_meses = np.round(clientes_9_meses, 0)
    clientes_20_meses = np.round(clientes_20_meses, 0)


    mx = np.array([clientes_iniciales, clientes_3_meses, clientes_5_meses, clientes_7_meses, clientes_9_meses,
                   clientes_20_meses])


    df = pd.DataFrame(mx, columns=['Clientes en A', 'Clientes en B', 'Clientes en C'])
    index = pd.Series([0, 3, 5, 7, 9, 20])
    df.set_index(index, inplace=True)
    df.index.name = 'Tiempo transcurrido [meses]'

    print(mx)

    graficar(mx=mx)






