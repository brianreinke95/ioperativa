from random import random
import matplotlib.pyplot as plt

p1 = 0.1
p2 = 0.15
p3 = 0.25
p4 = 0.35
p5 = 0.15

dias = 100

t = range(0, dias)
eventos = []
n = 0
while n < dias:
    r = random()
    if r <= 0.1:
        eventos.append(1)
    elif r < 0.25:
        eventos.append(2)
    elif r < 0.5:
        eventos.append(3)
    elif r < 0.85:
        eventos.append(4)
    else:
        eventos.append(5)
    n += 1
eventos_ordenados = eventos.copy()
eventos_ordenados.sort()
n = 5
vec_n = range(1, n + 1)
vec_ocurrencias = [eventos_ordenados.count(i) for i in range(1, n + 1)]
print(vec_ocurrencias)

plt.subplot(121)
plt.bar(t, eventos)
plt.title('Eventos ocurridos', loc='right')
plt.ylabel('Nro Asistencias')
plt.xlabel('Dias')

plt.subplot(122)
plt.bar(vec_n, vec_ocurrencias)
plt.title('Ocurrencias', loc='right')
plt.ylabel('ocurrencias')
plt.xlabel('Nro de asistencias')
plt.show()
