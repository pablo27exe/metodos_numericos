# Importar la clase Fraction para trabajar con fracciones
from fractions import Fraction
pasos = 1

# Función para convertir una lista de strings en fracciones
def fila_a_fracciones(valores):
    # Usamos comprensión de listas para convertir cada número a Fraction
    return [Fraction(Numeros) for Numeros in valores]

# mostrar la matriz en pantalla
def enseñar_matriz(Matriz):
    global pasos
    print('---------------------------------------------')
    print(f'Paso {pasos}:')
    # Recorrer cada fila de la matriz
    for fila in Matriz:
        # Mostrar los valores de la fila
        print(" ".join(str(x) for x in fila))
    print()
    pasos +=1

# Función que se encarga de realizar el Gauss-Jordan por pasos
def gauss_jordan(Matriz):
    # Se guardan el número de filas
    filas = len(Matriz)
    # Se guarda el número de columnas
    columnas = len(Matriz[0])
    # Índice de la primer fila pivote
    pivoteF = 0

    # Se recorre cada columna
    for col in range(columnas):
        # Si ya no hay más filas se acaba :)
        if pivoteF >= filas:
            break

        #buscar una fila con pivote no nulo en esta columna, esta parte sirve para poder identificar la fila que se va a operar en ese momento, se hace uso del ciclo para que recorra unicamente las filas que no han sido convertidas a 0 y 1. La condición evalua si se encuentra algo diferente a 0, lo que indica que se puede trabajar con la fila para operarla. a la fila encontrada se le asigna el valor de r (es decir la primera fila que encotró con base en la condición) y hace uso de break ya que no necesita seguir buscando más filas.
        
        fila_encontrada = None
        for r in range(pivoteF, filas):
            if Matriz[r][col] != 0:
                fila_encontrada = r
                break

        # complementa a lo anterior, es decir que si en el paso anterior no se encontró ninguna fila en esta columna que tuviera un valor distinto de cero. Quiere decir que si en la columna no hay ceros no hay pivote y pasa a otro. No hace ninguna operación
        if fila_encontrada is None:
            continue

        #se evaluea si la fila donde se encontró el pivote es distinta de la fila actual donde se tiene que poner
        #Si son iguales quiere decir que ya se tiene el pivote en la posición correcta
        #Si son diferentes se tiene que hacer un intercambio de filas.
        if fila_encontrada != pivoteF:
            Matriz[pivoteF], Matriz[fila_encontrada] = Matriz[fila_encontrada], Matriz[pivoteF]
            print(f"Intercambio fila {pivoteF+1} <-> fila {fila_encontrada+1}")
            enseñar_matriz(Matriz)

        # Se realizan las operaciones para hacer que el pivote se convierta a 1
        pivote = Matriz[pivoteF][col] #toma el valor actual del pivote
        if pivote != 1: #Se considera evaluar si el valor ya es 1 si lo es no hace la operación
            Matriz[pivoteF] = [x / pivote for x in Matriz[pivoteF]]#esta parte realiza el proceso donde se hace uso de la formula a * 1/a 
            print(f"F{pivoteF+1} / {pivote}")
            print()
            enseñar_matriz(Matriz)

        # Se convierten a 0 las demás filas de la columna
        for cola in range(filas): #se recorren de nuevo todas las filas de la matriz
            if cola != pivoteF: #omite la fila pivote ya que ya se convirtió a 1 y ya no se toca
                Numero_para_restar = Matriz[cola][col] #se toma el valor que está en la columna del pivote de la fila en la que se está actualmente
                if Numero_para_restar != 0: #Si ya es ceero no se hace nada
                    Matriz[cola] = [Matriz[cola][c] - Numero_para_restar * Matriz[pivoteF][c] for c in range(columnas)] #esta parte se encarga de realizar la formula Fn - Factor(Fa) es decir la columna menos el inverso sumativo del factor por la fila pivote

                    #Se imprime la formula
                    print(f"Columna{cola+1} = Columna{cola+1} - ({Numero_para_restar})*COlumna{pivoteF+1}")
                    print()
                    enseñar_matriz(Matriz)

        # Se avanza a la siguiente fila pivote
        pivoteF += 1

    # Al final se muestra la matriz
    print("Matriz final")
    enseñar_matriz(Matriz)

