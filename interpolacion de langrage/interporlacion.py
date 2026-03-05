
import numpy as np
import matplotlib.pyplot as plt

# Datos conocidos con 8 nodos 
x = np.array([1, 2, 3, 4, 5, 6, 7, 8,9,10,11,12,13,14,15,16,17, 18, 19, 20,21])
y = np.array([8,6, 2, 9, 1, 5, 4, 7,3,6,8, 4, 1, 3, 4,5,6,3,8,1,2])

# Función de interpolación de Lagrange
def lagrange(xi, yi, x_eval):
    n = len(xi)
    P = np.zeros_like(x_eval, dtype=float)
    for i in range(n):
        L = np.ones_like(x_eval, dtype=float)
        for j in range(n):
            if i != j:
                L *= (x_eval - xi[j]) / (xi[i] - xi[j])
        P += yi[i] * L
    return P

# Evaluación en 300 puntos para mayor resolución desde 1 a 8
x_eval = np.linspace(1, 21, 100) 
y_eval = lagrange(x, y, x_eval)

# Gráfica
plt.figure(figsize=(8, 5))
plt.plot(x_eval, y_eval, 'b-', label='Polinomio de Lagrange')
plt.plot(x, y, 'ro', label='Datos originales')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Interpolación Polinómica - Lagrange con 8 nodos enteros')
plt.legend()
plt.grid(True)
plt.show()
