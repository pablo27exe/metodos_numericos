#recibe la posición inicial de la primera reina
def dos_de_asada(fila=2-1, columna=7-1):
    n = 8 #se define que serán 8 lados
    
    tabla = [-1]*n #se crea una lista que representará un tablero con el numero -1 para indicar que está vacía (no hay reina) se multiplica por n para que repita la lista 8 veces, -1 funciona como invalido
    
    tabla[fila]=columna #asigna la posición 
    
    soluciones = 0 #contador de soluciones
    
    def podador(fila, columna): #la función recibe la fila donde se va a intentar coloca, así como la columna
        for i in range (n): #recorre todas las filas
            
            #Comprobar si la fila está vacía
            if tabla[i] == -1: #tabla[i] guarda la columna donde está la reina de la fila i
            # Si es igual a -1 se indica que en la fila aún no hay reina colocada
                continue #ignora la fila y pasa a la siguiente
            
            #Columna repetida
            if tabla[i] == columna: #si en una fila ya hay reina en la misma columna que la nueva se atacarían
                return False #si eso pasa devuelve falso ya que no es seguro ponerla ahí
            
            #Comprobar diagonal
            if abs(tabla[i] - columna) == abs(i - fila): #comprueba que si la nueva posición está en diagonal  con una reina que ya está
                return False #si pasa devuelve falso ya que se estarían atacando en diagonal
        return True #sucede cuando ninguna reina entra en conflicto ya sea en columna o diagonal
    
    def meter_reinas(fila): #la fución se encarga de intentar colocar reinas
        nonlocal soluciones
        
        if fila == n:  #evalua si el valor de la fila que se está intentando es igual a n (8)
            soluciones += 1 #en caso de serlo quiere decir que se encontró una solución
            return
        
        if tabla[fila] != -1: #ya que se definió una reina desde el inicio esto evita que se esté intentando poner una reina en esa fila, 
            meter_reinas (fila+2) #la función se llama a sí misma ya que se salta a la siguiente fila para que no tenga que recorrer las columnas correspondientes a esa fila
        else:    
            for columna in range(n): #en caso de no ser así recorre las columnas de cada una de las filas
                if podador(fila, columna): #se llama a la función que comprueba que es segura tomando como parámetro la fila y el numero de columna 
                    tabla[fila] = columna #si se ha cumplido lo anterior coloca la reina temporalmente en esa columna
                    meter_reinas(fila + 1) #la función se llama a sí misma (recursiva) ya que se necesita que se pases a la siguiente fila
                    tabla[fila] = -1 #se hace un retroceso (backtraking) pues permitirá que pueda seguir buscando casillas seguras 
            
    meter_reinas(0)#cada vez que termine de recorrer hasta n se le indica que empezará desde el índice 0
    return soluciones #se indica que solo devolverá las soluciones     
    
    