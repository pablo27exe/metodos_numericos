import matplotlib.pyplot as plt
import numpy as np

def f(x):
    return x**2 -2

def df(x):
    return 2*x

x_vals = []
errors_abs = []
errors_rel = []
    
x0 = 1
x_vals.append(x0)

for i in range(10):
    x1 = x0 - f(x0)/df(x0)
    x_vals.append(x1)
    ea = abs(x1-x0)
    er = ea / abs(x1)
    errors_abs.append(ea)
    errors_rel.append(er)
    x0 = x1
    
#grafica de f(x)
plt.figure()
x = np.linspace(0, 2, 100)
plt.plot(x, f(x), 'b-', linewidth=2, label='f(x) = x² - 2')
plt.axhline(0, color='black', linestyle='-', alpha=0.3)
plt.axvline(np.sqrt(2), color='red', linestyle='--', linewidth=2, label='Raíz exacta (√2)')
plt.scatter(x_vals, [f(x) for x in x_vals], color='red', s=50, zorder=5, label='Aproximaciones')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.title('Gráfica de f(x) = x² - 2')
plt.grid(True, alpha=0.3)
plt.savefig('grafica_funcion.png')
plt.close()  # ← AGREGAR

# Gráfica de aproximaciones
plt.figure()
plt.plot(x_vals, marker='o')
plt.title('Aproximaciones sucesivas')
plt.xlabel('Iteración')
plt.ylabel('x_n')
plt.grid(True, alpha=0.3)
plt.savefig('grafica_aproximaciones.png')
plt.close()  # ← AGREGAR

# Error absoluto
plt.figure()
plt.plot(errors_abs, marker='o')
plt.title('Error absoluto por iteración')
plt.xlabel('Iteración')
plt.ylabel('Error absoluto')
plt.grid(True, alpha=0.3)
plt.savefig('grafica_error_absoluto.png')
plt.close()  # ← AGREGAR

# Error relativo
plt.figure()
plt.plot(errors_rel, marker='o')
plt.title('Error relativo por iteración')
plt.xlabel('Iteración')
plt.ylabel('Error relativo')
plt.grid(True, alpha=0.3)
plt.savefig('grafica_error_relativo.png')
plt.close()  # ← YA ESTÁ