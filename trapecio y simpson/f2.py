import numpy as np
import matplotlib.pyplot as plt

def trapecio_compuesto(f, a, b, n):
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    suma = y[0] + y[-1]
    for i in range(1, n):
        suma += 2 * y[i]
    return (h / 2) * suma, x, y

def simpson_compuesto(f, a, b, n):
    if n % 2 != 0: 
        n += 1  # Asegurar que n sea par
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    suma = y[0] + y[-1]
    for i in range(1, n):
        if i % 2 == 1:  # índices impares
            suma += 4 * y[i]
        else:  # índices pares
            suma += 2 * y[i]
    return (h / 3) * suma, x, y

# Segunda función a integrar: I2 = ∫₀³ x² dx
f2 = lambda x: x**2

# Parámetros
a, b, exacto = 0, 3, 9.0
n_values = [2, 4, 8, 16, 32]

# Listas para almacenar errores
errores_simpson = []
errores_trapecio = []
aproximaciones_simpson = []
aproximaciones_trapecio = []

print("RESULTADOS COMPARATIVOS - I2 = ∫₀³ x² dx")
print("n\tSimpson\t\tError Simpson\tTrapecio\tError Trapecio")
print("-" * 80)

for n in n_values:
    # Simpson
    aproximacion_s, x_puntos_s, y_puntos_s = simpson_compuesto(f2, a, b, n)
    error_s = abs(exacto - aproximacion_s)
    
    # Trapecio
    aproximacion_t, x_puntos_t, y_puntos_t = trapecio_compuesto(f2, a, b, n)
    error_t = abs(exacto - aproximacion_t)
    
    # Almacenar resultados
    errores_simpson.append(error_s)
    errores_trapecio.append(error_t)
    aproximaciones_simpson.append(aproximacion_s)
    aproximaciones_trapecio.append(aproximacion_t)
    
    print(f"{n}\t{aproximacion_s:.6f}\t{error_s:.6f}\t{aproximacion_t:.6f}\t{error_t:.6f}")
    
    # Gráfica individual para Simpson
    plt.figure(figsize=(12, 8))
    x_fine = np.linspace(a, b, 200)
    y_fine = f2(x_fine)
    
    # Curva de la función
    plt.plot(x_fine, y_fine, 'b-', linewidth=3, label='f(x) = x²')
    
    # Puntos de evaluación
    plt.plot(x_puntos_s, y_puntos_s, 'ro-', markersize=8, linewidth=2, label='Puntos de evaluación')
    
    # Aproximaciones parabólicas de Simpson
    for i in range(0, n, 2):
        # Puntos para la parábola
        x_parab = np.linspace(x_puntos_s[i], x_puntos_s[i+2], 50)
        # Interpolación cuadrática para Simpson
        coef = np.polyfit([x_puntos_s[i], x_puntos_s[i+1], x_puntos_s[i+2]], 
                         [y_puntos_s[i], y_puntos_s[i+1], y_puntos_s[i+2]], 2)
        parab = np.poly1d(coef)
        y_parab = parab(x_parab)
        
        # Rellenar área bajo la parábola
        plt.fill_between(x_parab, y_parab, alpha=0.3, color='lightgreen', 
                        label='Aproximación parabólica' if i == 0 else "")
        
        # Dibujar la parábola
        plt.plot(x_parab, y_parab, 'g--', linewidth=2, alpha=0.8)
    
    plt.axhline(y=0, color='black', linewidth=1, alpha=0.5)
    plt.xlabel('x', fontsize=12)
    plt.ylabel('f(x)', fontsize=12)
    plt.title(f'Método de Simpson 1/3 Compuesto - I2 = ∫₀³ x² dx\nn = {n} | Aproximación: {aproximacion_s:.6f} | Error: {error_s:.6f}', 
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xlim(a, b)
    plt.ylim(-0.5, 10.5)
    plt.xticks(np.arange(0, 3.5, 0.5))
    plt.yticks(np.arange(0, 11, 1))
    plt.grid(True, which='both', alpha=0.2)
    plt.tight_layout()
    plt.show()
    
    # Gráfica individual para Trapecio
    plt.figure(figsize=(10, 6))
    x_fine = np.linspace(a, b, 100)
    y_fine = f2(x_fine)
    
    # Curva de la función
    plt.plot(x_fine, y_fine, 'b-', linewidth=2, label='x²')
    
    # Puntos de evaluación
    plt.plot(x_puntos_t, y_puntos_t, 'ro-', markersize=6, label='Puntos de evaluación')
    
    # Trapecios
    for i in range(n):
        plt.fill([x_puntos_t[i], x_puntos_t[i], x_puntos_t[i+1], x_puntos_t[i+1]], 
                 [0, y_puntos_t[i], y_puntos_t[i+1], 0], 'orange', alpha=0.5, 
                 label='Trapecios' if i == 0 else "")
    
    plt.xlabel('x', fontsize=12)
    plt.ylabel('f(x)', fontsize=12)
    plt.title(f'Método del Trapecio Compuesto - I2 = ∫₀³ x² dx\nn = {n} | Aproximación: {aproximacion_t:.4f} | Error: {error_t:.4f}',
              fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xlim(a, b)
    plt.ylim(0, 10)
    plt.xticks(np.arange(0, 3.5, 0.5))
    plt.yticks(np.arange(0, 11, 1))
    plt.tight_layout()
    plt.show()

# GRÁFICA COMPARATIVA DE ERRORES
plt.figure(figsize=(12, 8))
plt.plot(n_values, errores_trapecio, 'ro-', linewidth=2, markersize=8, label='Error Trapecio')
plt.plot(n_values, errores_simpson, 'bo-', linewidth=2, markersize=8, label='Error Simpson')

plt.xlabel('Número de subintervalos (n)', fontsize=12)
plt.ylabel('Error absoluto', fontsize=12)
plt.title('Comparación de Error: Trapecio vs Simpson 1/3\nI₂ = ∫₀³ x² dx (Simpson: Error = 0 para todo n)', 
          fontsize=14, fontweight='bold')
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.yscale('log')  # Escala logarítmica
plt.xscale('log')  # Escala logarítmica

# Añadir valores en los puntos
for i, n in enumerate(n_values):
    plt.annotate(f'{errores_trapecio[i]:.2e}', (n, errores_trapecio[i]), 
                textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)
    # Para Simpson, mostrar que es 0
    plt.annotate('0.00', (n, errores_simpson[i]), 
                textcoords="offset points", xytext=(0,-15), ha='center', fontsize=9)

plt.tight_layout()
plt.show()

# Tabla resumen de errores
print("\n" + "="*80)
print("TABLA RESUMEN DE ERRORES - I₂ = ∫₀³ x² dx")
print("="*80)
print("n\tTrapecio\t\tSimpson\t\t\tMejor Método")
print("-"*80)
for i, n in enumerate(n_values):
    mejor = "Trapecio" if errores_trapecio[i] < errores_simpson[i] else "Simpson"
    print(f"{n}\t{errores_trapecio[i]:.2e}\t\t{errores_simpson[i]:.2e}\t\t{mejor}")
