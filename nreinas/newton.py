import pandas as pd
import numpy as np
import sympy as sp
from sympy import sympify, lambdify

class MetodoNewtonRaphson:
    def __init__(self):
        self.x = sp.symbols('x')
        self.funcion = None
        self.funcion_derivada = None
        self.f_lambda = None
        self.f_prime_lambda = None
        
    def definir_funcion(self, expr_str):
        """
        Define la función y su derivada a partir de una expresión string
        
        Args:
            expr_str (str): Expresión matemática en términos de 'x'
        """
        try:
            # Convertir string a expresión sympy
            expr = sympify(expr_str)
            self.funcion = expr
            
            # Calcular derivada
            self.funcion_derivada = sp.diff(expr, self.x)
            
            # Convertir a funciones lambda para evaluación numérica
            self.f_lambda = lambdify(self.x, expr, 'numpy')
            self.f_prime_lambda = lambdify(self.x, self.funcion_derivada, 'numpy')
            
            print(f"Función definida: f(x) = {expr}")
            print(f"Derivada: f'(x) = {self.funcion_derivada}")
            
        except Exception as e:
            print(f"Error al procesar la función: {e}")
            return False
        return True
    
    def newton_raphson(self, x0, tol=1e-6, max_iter=100):
        """
        Aplica el método de Newton-Raphson
        
        Args:
            x0 (float): Valor inicial
            tol (float): Tolerancia para la convergencia
            max_iter (int): Número máximo de iteraciones
            
        Returns:
            pd.DataFrame: Tabla con resultados de cada iteración
            float: Raíz aproximada
        """
        if self.f_lambda is None:
            print("Primero debe definir una función")
            return None, None
        
        datos_iteraciones = []
        x_actual = x0
        
        for i in range(max_iter):
            try:
                f_x = self.f_lambda(x_actual)
                f_prime_x = self.f_prime_lambda(x_actual)
                
                # Evitar división por cero
                if abs(f_prime_x) < 1e-10:
                    print("Derivada cercana a cero. Método puede divergir.")
                    break
                
                x_siguiente = x_actual - f_x / f_prime_x
                error = abs(x_siguiente - x_actual)
                
                # Guardar datos de la iteración
                datos_iteraciones.append({
                    'Iteración': i + 1,
                    'x_n': x_actual,
                    'f(x_n)': f_x,
                    "f'(x_n)": f_prime_x,
                    'x_{n+1}': x_siguiente,
                    'Error': error
                })
                
                # Verificar convergencia
                if error < tol:
                    print(f"Convergencia alcanzada en {i + 1} iteraciones")
                    break
                
                x_actual = x_siguiente
                
            except Exception as e:
                print(f"Error en iteración {i + 1}: {e}")
                break
        
        else:
            print("Máximo número de iteraciones alcanzado")
        
        # Crear DataFrame con los resultados
        df_resultados = pd.DataFrame(datos_iteraciones)
        return df_resultados, x_actual
    
    def graficar_funcion(self, x_min, x_max, num_puntos=1000):
        """
        Grafica la función (requiere matplotlib)
        """
        try:
            import matplotlib.pyplot as plt
            
            x_vals = np.linspace(x_min, x_max, num_puntos)
            y_vals = self.f_lambda(x_vals)
            
            plt.figure(figsize=(10, 6))
            plt.plot(x_vals, y_vals, 'b-', label=f'f(x) = {self.funcion}')
            plt.axhline(y=0, color='k', linestyle='--', alpha=0.7)
            plt.axvline(x=0, color='k', linestyle='--', alpha=0.7)
            plt.grid(True, alpha=0.3)
            plt.xlabel('x')
            plt.ylabel('f(x)')
            plt.title('Gráfica de la función')
            plt.legend()
            plt.show()
            
        except ImportError:
            print("Matplotlib no está instalado. No se puede graficar.")
        except Exception as e:
            print(f"Error al graficar: {e}")

# Listado de funciones de ejemplo
FUNCIONES_EJEMPLO = {
    "1": "x**3 - 2*x - 5",                    # Raíz cerca de 2.0946
    "2": "exp(x) - 3*x",                      # Raíz cerca de 0.6191 y 1.5121
    "3": "cos(x) - x",                        # Raíz cerca de 0.7391
    "4": "x**2 - 2",                          # Raíz en √2 ≈ 1.4142
    "5": "x**3 + 4*x**2 - 10",                # Raíz cerca de 1.3652
    "6": "sin(x) - x/2",                      # Raíz no trivial cerca de ±1.8955
    "7": "log(x+1) - cos(x)",                 # Raíz cerca de 0.5
    "8": "x*exp(-x) - 0.2",                   # Raíz cerca de 0.2592 y 2.5426
}

def mostrar_funciones_ejemplo():
    """Muestra las funciones de ejemplo disponibles"""
    print("\n=== FUNCIONES DE EJEMPLO ===")
    for key, func in FUNCIONES_EJEMPLO.items():
        print(f"{key}: f(x) = {func}")
    print()

def main():
    """Función principal para ejecutar el método"""
    metodo = MetodoNewtonRaphson()
    
    while True:
        print("\n=== MÉTODO DE NEWTON-RAPHSON ===")
        print("1. Usar función de ejemplo")
        print("2. Ingresar función manualmente")
        print("3. Salir")
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "3":
            break
            
        elif opcion == "1":
            mostrar_funciones_ejemplo()
            seleccion = input("Seleccione el número de la función: ").strip()
            if seleccion in FUNCIONES_EJEMPLO:
                funcion_str = FUNCIONES_EJEMPLO[seleccion]
                if metodo.definir_funcion(funcion_str):
                    ejecutar_calculos(metodo)
            else:
                print("Selección inválida")
                
        elif opcion == "2":
            funcion_str = input("Ingrese la función f(x) (use 'x' como variable): ").strip()
            if metodo.definir_funcion(funcion_str):
                ejecutar_calculos(metodo)
                
        else:
            print("Opción inválida")

def ejecutar_calculos(metodo):
    """Ejecuta los cálculos una vez definida la función"""
    try:
        # Solicitar valor inicial
        x0 = float(input("Ingrese el valor inicial x0: "))
        
        # Solicitar parámetros opcionales
        tol_input = input("Tolerancia (default 1e-6): ").strip()
        tol = float(tol_input) if tol_input else 1e-6
        
        max_iter_input = input("Máximo iteraciones (default 100): ").strip()
        max_iter = int(max_iter_input) if max_iter_input else 100
        
        # Ejecutar método
        df, raiz = metodo.newton_raphson(x0, tol, max_iter)
        
        if df is not None:
            print("\n=== RESULTADOS ===")
            print(f"Raíz aproximada: {raiz}")
            print(f"f({raiz}) = {metodo.f_lambda(raiz)}")
            
            print("\n=== TABLA DE ITERACIONES ===")
            # Formatear DataFrame para mejor visualización
            pd.set_option('display.float_format', '{:.6f}'.format)
            print(df.to_string(index=False))
            
            # Preguntar si desea graficar
            graficar = input("\n¿Desea graficar la función? (s/n): ").strip().lower()
            if graficar == 's':
                x_min = float(input("Límite inferior para graficar: "))
                x_max = float(input("Límite superior para graficar: "))
                metodo.graficar_funcion(x_min, x_max)
                
    except ValueError:
        print("Error: Ingrese valores numéricos válidos")
    except Exception as e:
        print(f"Error durante los cálculos: {e}")

if __name__ == "__main__":
    main()