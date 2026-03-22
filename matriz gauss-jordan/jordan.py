arreglo = [-2,-6,-4,-4,-12,-8] 
arreglo_2 =[-2,-6,-4,-4,-12,-8] 
#arreglo = [9,-7,32,-5,13,405] 
#arreglo_2 = [9,-7,32,-5,13,405]   
fila_1 = []
fila_2 = []

def imprimir_matriz_2x3():
    
    for i in range(2):  # 2 filas
        for j in range(3):  # 3 columnas
            print(f"{arreglo[i*3 + j]:4}", end=" ")
        print()  # Salto de línea después de cada fila
    
imprimir_matriz_2x3()

def obtener_filas():
    global fila_1,fila_2
    
    fila_1 = arreglo[:3]
    fila_2 = arreglo[3:]
     

def acomodador_de_matrices():
    #paso1 inverso multiplicativo del pibote
    inverso_multiplicativo_uno=1/arreglo[0]
    #print(inverso_multiplicativo_uno)
    
    print("\nPrimer paso")
    for i in range(3):
        print(f'{arreglo[i]}x{inverso_multiplicativo_uno}')
        arreglo[i] = arreglo[i]*inverso_multiplicativo_uno
    print()  
    
    imprimir_matriz_2x3()
    obtener_filas()
    
    #paso 2 inverso sumativo
    inverso_sumativo = arreglo[3]*-1
    #print(inverso_sumativo)
    print("\nSegundo paso")
    for i in range(3):
        print(f'{arreglo[3 + i]} + {inverso_sumativo * fila_1[i]}')
        nuevo_valor = arreglo[3 + i] + (inverso_sumativo * fila_1[i])
        arreglo[3 + i] = nuevo_valor
        
    print()
    imprimir_matriz_2x3()
    obtener_filas()
    
    #paso 3 dividir por el segundo pivote
    segundo_pivote = arreglo[4]
    try:
        print("\nTercer paso")
        for i in range(3):
            print(f'{arreglo[3+i]}/{segundo_pivote} ')
            arreglo[3+i] = arreglo[3+i]/segundo_pivote 
    except:
        print('Error: No divisible entre 0')
        return
        
    print()
    imprimir_matriz_2x3()
    obtener_filas()
    
    #paso 4 segundo inverso sumativo
    seg_inverso_sumativo = arreglo[1]*-1
    #print(seg_inverso_sumativo)
    print("\nCuarto paso")
    for i in range(3):
        print(f'{arreglo[0 + i]} + {seg_inverso_sumativo * fila_2[i]}')
        nuevo_valor = arreglo[0 + i] + (seg_inverso_sumativo * fila_2[i])
        arreglo[0 + i] = nuevo_valor
        
    print()
    imprimir_matriz_2x3()
    obtener_filas()
    
    #comprobar resultados
    print(f'Ecuación: {arreglo_2[0]}*{arreglo[2]} + {arreglo_2[1]}*{arreglo[5]}')
    resultado = (arreglo_2[0]*arreglo[2]) + (arreglo_2[1]*arreglo[5])
    print()
    
    return resultado