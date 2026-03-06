from GJ import fila_a_fracciones, enseñar_matriz, gauss_jordan

# Pedir filas
n_filas = int(input("Número de filas: "))
# Pedir columnas
n_columnas = int(input("Número de columnas: "))

# Crear lista vacía para la matriz
matriz = []

# Se recorre cada fila para pedir los numeros
for i in range(n_filas):
    metida = input(f"Fila {i+1} (ingrese {n_columnas} números separados por espacios): ")
    # Separar por espacios
    valores = metida.split()
    # Convertir a fracciones
    fila = fila_a_fracciones(valores)
    # Agregar la fila a la matriz
    matriz.append(fila)

# Mostrar la matriz inicial
print("Matriz inicial:")
enseñar_matriz(matriz)

# Se ejecuta la funcion principal que realiza el calculo
gauss_jordan(matriz)