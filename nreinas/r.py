def hola(fila=2-1, columna=7-1):
    n = 8
    tablero = [-1] * n
    tablero[fila] = columna
    soluciones = 0
    
    def segura(fila, columna):
        for i in range(n):
            if tablero[i] == -1:
                continue
            if tablero[i] == columna:
                return False
            if abs(tablero[i] - columna) == abs(i - fila):
                return False
        return True
    
    def imprimir_tablero():
        for i in range(n):
            fila_str = ""
            for j in range(n):
                if tablero[i] == j:
                    fila_str += " Q "  # Reina
                else:
                    fila_str += " . "  # Casilla vacía
            print(fila_str)
        print("\n" + "-"*25 + "\n")  # Separador de soluciones
    
    def reinas(fila_actual):
        nonlocal soluciones
        if fila_actual == n:
            soluciones += 1
            print(f"Solución #{soluciones}:")
            imprimir_tablero()
            return
        
        if tablero[fila_actual] != -1:
            reinas(fila_actual + 1)
        else:
            for columna_actual in range(n):
                if segura(fila_actual, columna_actual):
                    tablero[fila_actual] = columna_actual
                    reinas(fila_actual + 1)
                    tablero[fila_actual] = -1  # B_]()
