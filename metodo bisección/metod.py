from dataclasses import dataclass, field
from typing import Optional, Tuple, List, Callable
import numpy as np
import matplotlib.pyplot as plt
import re
import sympy as sp



@dataclass
class ResultadoBiseccion:
    raiz: float
    iteraciones: int
    historial: List[Tuple[float, float, float, float, float]]
    convergio: bool
    error_final: float

@dataclass
class Biseccion:
    f: Callable[[float], float]
    a: float
    b: float
    tolerancia: float = 1e-6
    max_iter: int = 50
    
    def resolver(self) -> ResultadoBiseccion:
        """Ejecuta el método de bisección"""
        
        # Verificar si alguno de los extremos es raíz exacta
        f_a = self.f(self.a)
        f_b = self.f(self.b)
        
        if abs(f_a) < self.tolerancia:
            return ResultadoBiseccion(
                raiz=self.a,
                iteraciones=0,
                historial=[],
                convergio=True,
                error_final=abs(f_a)
            )
        
        if abs(f_b) < self.tolerancia:
            return ResultadoBiseccion(
                raiz=self.b,
                iteraciones=0,
                historial=[],
                convergio=True,
                error_final=abs(f_b)
            )
        
        # Verificar que f(a) y f(b) tengan signos opuestos
        if f_a * f_b >= 0:
            raise ValueError(f"La función debe tener signos opuestos en los extremos del intervalo [a, b]. f(a)={f_a:.6f}, f(b)={f_b:.6f}")
        
        # diseño para cada iteración de la bisección
        historial = []
        a_actual = self.a
        b_actual = self.b
        convergio = False
        error_actual = float('inf')
        
        for iteracion in range(1, self.max_iter + 1):
            # Calcular punto medio
            c = (a_actual + b_actual) / 2
            f_c = self.f(c)
            
            # Calcular error (diferencia entre iteraciones)
            if iteracion > 1:
                error_actual = abs(c - c_anterior)
            else:
                error_actual = abs(b_actual - a_actual)
            
            # Guardar para el historial de iteraciones
            historial.append((iteracion, a_actual, b_actual, c, error_actual))
            
            # Verificar convergencia (se acerca a la raíz real)
            if abs(f_c) < self.tolerancia or error_actual < self.tolerancia:
                convergio = True
                break
            
            # Actualizar intervalo
            if f_a * f_c < 0:
                b_actual = c
                f_b = f_c
            else:
                a_actual = c
                f_a = f_c
            
            c_anterior = c
        
        #devolver los datos importantes para su impresión
        return ResultadoBiseccion(
            raiz=c,
            iteraciones=iteracion,
            historial=historial,
            convergio=convergio,
            error_final=error_actual
        )

    #muestra en forma de tabla los resultados
    def mostrar_resultados(self, resultado: ResultadoBiseccion) -> None:
        """Muestra los resultados enfocados en iteraciones y error"""
        print("\nRESULTADOS DEL MÉTODO DE BISECCIÓN")
        print("=" * 60)
        print(f"Iteraciones realizadas: {resultado.iteraciones}")
        print(f"Raíz aproximada: {resultado.raiz:.10f}")
        print(f"Error final: {resultado.error_final:.2e}")
        print(f"¿Convergió?: {'Sí' if resultado.convergio else 'No'}")
        
        print("\nDETALLE DE ITERACIONES")
        print("=" * 60)
        print(f"{'Iter':<6} {'a':<12} {'b':<12} {'c':<12} {'Error':<15}")
        print("-" * 60)
        
        for iteracion, a, b, c, error in resultado.historial:
            print(f"{iteracion:<6} {a:<12.6f} {b:<12.6f} {c:<12.6f} {error:<15.2e}")
     
    #diseño de la gráfica, (en caso de funciones como seno, coseno, etc usará pi)       
    def graficar(self, resultado: ResultadoBiseccion, ancho: float = 2.0) -> None:
        """Grafica la función y el proceso de bisección"""
        
        # Crear rango para graficar
        x_min = min(self.a, self.b, resultado.raiz) - ancho
        x_max = max(self.a, self.b, resultado.raiz) + ancho
        x_vals = np.linspace(x_min, x_max, 1000)
        y_vals = [self.f(x) for x in x_vals]
        
        fig, ax = plt.subplots(figsize=(10, 6))
    
        # Gráfico de la función
        ax.plot(x_vals, y_vals, 'b-', linewidth=2, label='f(x)')
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax.axvline(x=resultado.raiz, color='r', linestyle='--', 
                label=f'Raíz ≈ {resultado.raiz:.6f}')
        ax.scatter([self.a, self.b], [self.f(self.a), self.f(self.b)], 
                color='green', s=100, zorder=5, label='Extremos')
        ax.scatter([resultado.raiz], [0], color='red', s=100, zorder=5, label='Raíz')
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title('Función y raíz encontrada')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()


# Función auxiliar para detectar funciones periódicas
def es_periodica(funcion_string: str) -> bool:
    patrones_trig = [r'sin\s*\(', r'cos\s*\(', r'tan\s*\(', r'csc\s*\(', r'sec\s*\(', r'cot\s*\(']
    for patron in patrones_trig:
        if re.search(patron, funcion_string, re.IGNORECASE):
            return True
    return False

# Función para formatear eje con π
def formatear_eje_pi(ax, x_min, x_max):
    """Formatea el eje x con valores en términos de π"""
    pi_multiplos = []
    etiquetas = []
    
    min_multiplo = int(np.ceil(x_min / np.pi))
    max_multiplo = int(np.floor(x_max / np.pi))
    
    for multiplo in range(min_multiplo, max_multiplo + 1):
        x_val = multiplo * np.pi
        pi_multiplos.append(x_val)
        
        if multiplo == 0:
            etiquetas.append('0')
        elif multiplo == 1:
            etiquetas.append('π')
        elif multiplo == -1:
            etiquetas.append('-π')
        else:
            etiquetas.append(f'{multiplo}π')
    
    ax.set_xticks(pi_multiplos)
    ax.set_xticklabels(etiquetas)
    
    for x_val in pi_multiplos:
        ax.axvline(x=x_val, color='gray', linestyle='--', alpha=0.3, linewidth=0.8)