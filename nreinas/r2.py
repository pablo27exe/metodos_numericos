def problema_reinas(fila=4,columna=4):
    n = 8
    
    tablero = [-1]*n
    
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
     
    def asignar(fila):
        nonlocal soluciones
        
        if fila == n:
            soluciones += 1
            return
        
        if tablero[fila] != -1:
            asignar(fila+1)
        else:
            for columna in range (n):
                if segura(fila, columna):
                    tablero[fila] = columna
                    asignar(fila+1)
                    tablero[fila] = -1
        
    asignar(0)
    return soluciones

solucion = problema_reinas()
print(f'El numero de soluciones si la primera reina está en 4,4 es:  {solucion}')

            

                
