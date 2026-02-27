def problema_reinas(fila=2,columna=7):
    n = 8
    
    tablero = [-1]*n
    
    tablero[fila] = columna
    
    soluciones = 0
    
    def  es_segura(fila,columna):
        for i in range(n):
            
            if tablero[i] == -1:
                continue
            if tablero[i] == columna:
                return False
            
            if abs(tablero[i] - columna) == abs(i- fila):
                return False
        return True
    
    def colocar(fila):
        nonlocal soluciones
        
        if fila == n:
            soluciones += 1
            return
        
        if tablero[fila] != -1:
            colocar(fila+1)
        else:
            for columna in range(n):
                if es_segura(fila,columna):
                    tablero[fila] = columna
                    colocar(fila+1)
                    tablero[fila] = -1
    
    colocar(0)
    return soluciones


hola = problema_reinas()
print(hola)
