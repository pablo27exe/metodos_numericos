from metod import Biseccion
import sympy as sp
import random

# Programa principal
if __name__ == "__main__":
    #Solicitar función al usuario
    entrada_funcion = input("Ingresa la función: ")
    x = sp.Symbol('x')
    funcion_simbolica = sp.sympify(entrada_funcion)
    f = sp.lambdify(x, funcion_simbolica, modules=["numpy"])

    #Selección de intervalo
    modo = input("¿Quieres ingresar los valores de a y b manualmente (m) o que se generen aleatoriamente (r)? ")

    if modo.lower() == 'm':
        a = float(input("Ingresa el valor de a: "))
        b = float(input("Ingresa el valor de b: "))
    else:
    # Generar valores aleatorios con signos opuestos en la función
        while True:
            a = random.uniform(-10, 10)
            b = random.uniform(-10, 10)
            
            # Asegurar que a < b
            if a > b:
                a, b = b, a
                
            # Verificar que f(a) y f(b) tengan signos opuestos
            f_a = f(a)
            f_b = f(b)
            
            if abs(f_a) < 1e-10:  # a es raíz
                break
            elif abs(f_b) < 1e-10:  # b es raíz
                a, b = b, b + 1  # ajustar para mantener intervalo válido
                break
            elif f_a * f_b < 0:  # signos opuestos
                break
                
            # Si no tienen signos opuestos, intentar de nuevo
            print(f"Intento: a={a:.4f}, b={b:.4f}, f(a)={f_a:.4f}, f(b)={f_b:.4f}")
        
        print(f"Valores generados: a = {a:.4f}, b = {b:.4f}")
        print(f"f(a) = {f(a):.6f}, f(b) = {f(b):.6f}")

    print(f"Usando intervalo: a = {a}, b = {b}")

    #resolución
    biseccion_solver = Biseccion(
        f=f,
        a=a,
        b=b,
        tolerancia=1e-6,
        max_iter=50
    )

    resultado = biseccion_solver.resolver()
    biseccion_solver.mostrar_resultados(resultado)
       
    # Preguntar si desea graficar
    biseccion_solver.graficar(resultado)