
from dataclasses import dataclass # la estructura de datos será con dataclasses
from typing import Optional, Tuple, List # Se usará para tipado fuerte
import sympy as sp #manipulación algebraica
import numpy as np #operaciones con arrays, operaciones matemáticas como derivadas
import matplotlib.pyplot as plt #se crerán gráficos
import re  # Importamos re para detectar funciones trigonométricas

#Clase: Represante cada paso que se realiza de manera iterativa al buscar raíces
@dataclass
class movida:
    n: int
    metodo: str #Se definirá posteriormente a "NR" Ccuando se use Newton-Raphson o "BIS" para la bisección
    x: float #valor de x en cada iteracion
    fx : float #valor de la función
    f_prima_x: Optional[float] #derivada de la función, es opcional ya que para la biseción debe de guardar NONE
    delta: Optional[float]  #tamaño del paso propuesto (en Newton-Raphson: -f(x)/f'(x)) muestra la magnitud y dirección del movimiento propuesto
    error: Optional[float]   #mide la diferencia absoluta entre la iteración actual y la anterior, mide la convergencia, para cuando el error es menor que una tolerancia
    descripcion: str #guardará toda la información para mostrarla en consola
    
#FUNCIONES COMPLEMENTARIAS
#Esta sección consta de la funcion que permite diseñar el formato de impresión además de funciones que permiten decidir cual es el mejor punto inicial

def _formato_descripcion(x,fx,f_prima_x,nuevo_x):
    return(f"x(n+1) = xn - f(xn)/f'(xn) = {x:.10f} - ({fx:.6e})/({f_prima_x:.6e}) = {nuevo_x:.10f}")
    #la función devuelve un string con el desglose de la formula
    
def _cambiooo(x:float) -> int:
    return 1 if x > 0 else (-1 if x < 0 else 0)
#esta función es importante para este caso donde se depende de cambios de signo se define como privada y recibe a x como número de entrada (decimal) y lo retorna como un entero lo que permite determinar el signo del número, lo que permite decidir cómo se ajustarán los límites del intervalo y detectar si hay raíz en el intervalo.

def _es_funcion_periodica(funcion_string: str) -> bool:
    """Detecta si la función contiene funciones trigonométricas"""
    patrones_trig = [r'sin\s*\(', r'cos\s*\(', r'tan\s*\(', r'csc\s*\(', r'sec\s*\(', r'cot\s*\(']
    for patron in patrones_trig:
        if re.search(patron, funcion_string, re.IGNORECASE):
            return True
    return False

def _formatear_eje_pi(ax, x_min, x_max):
    """Formatea el eje x con valores en términos de π"""
    # Determinar los múltiplos de π dentro del rango visible
    pi_multiplos = []
    etiquetas = []
    
    # Calcular los múltiplos enteros de π dentro del rango
    min_multiplo = int(np.ceil(x_min / np.pi))
    max_multiplo = int(np.floor(x_max / np.pi))
    
    for multiplo in range(min_multiplo, max_multiplo + 1):
        x_val = multiplo * np.pi
        pi_multiplos.append(x_val)
        
        # Crear etiquetas bonitas
        if multiplo == 0:
            etiquetas.append('0')
        elif multiplo == 1:
            etiquetas.append('π')
        elif multiplo == -1:
            etiquetas.append('-π')
        elif multiplo > 0:
            etiquetas.append(f'{multiplo}π')
        else:
            etiquetas.append(f'{multiplo}π')
    
    # Ordenar y eliminar duplicados
    pi_multiplos, indices_unicos = np.unique(pi_multiplos, return_index=True)
    etiquetas = [etiquetas[i] for i in indices_unicos]
    
    # Configurar los ticks del eje x
    ax.set_xticks(pi_multiplos)
    ax.set_xticklabels(etiquetas)
    
    # Añadir líneas verticales en los múltiplos de π
    for x_val in pi_multiplos:
        ax.axvline(x=x_val, color='gray', linestyle='--', alpha=0.3, linewidth=0.8)

def encontrar_intervalos(f_num, intervalo=(-100,100), pasos=2000, es_periodica=False):
    a , b = intervalo
    puntos_equidistantes = np.linspace(a,b,pasos) #crear un array con la variable de pasos como puntos que equidistan
    evaluacion = f_num(puntos_equidistantes) #evalua la funcion en todos los puntos
    
    rangos = [] #se crea una lista donde se almacenan los intervalos
    
    # Verificar si hay raíces en puntos donde la función cruza el eje x sin cambio de signo
    # (como en x=0 para x**3 donde f(0)=0 pero no hay cambio de signo)
    for i in range(len(puntos_equidistantes)):
        if abs(evaluacion[i]) < 1e-10:  # Si la función es muy cercana a cero
            # Crear un intervalo pequeño alrededor del punto donde f(x) ≈ 0
            punto_cercano = puntos_equidistantes[i]
            rangos.append((punto_cercano - 0.1, punto_cercano + 0.1))
    
    for i in range(len(puntos_equidistantes)-1):#va a recorrerse en base la longitud del array de puntos
        if np.isfinite(evaluacion[i]) and np.isfinite(evaluacion[i+1]) and _cambiooo(evaluacion[i]) * _cambiooo(evaluacion[i+1]) < 0:
            rangos.append((puntos_equidistantes[i],puntos_equidistantes[i+1]))
          
        #la condición tiene tres partes
        #np.isfinite(evaluacion[i]) verifica que el valor en el punto i no sea infinito ni NaN
        #np.isfinite(evaluacion[i+1]) verifica que el valor en el pinto i+1 no sea infinito ni NaN
        #_cambiooo(evaluacion[i]) * _cambiooo(evaluacion[i+1]) < 0 Detecta cambio de signo entre puntos consecutivos
        #Teorema del Valor Intermedio (TVI)
        #Si f es continua en [a, b] y f(a)*f(b) < 0,
        #entonces existe al menos una raíz en (a, b)
        #si bien detecta raíces en automático puede perder raíces si el espaciado es muy grande

    # Eliminar intervalos duplicados o muy cercanos
    rangos_unicos = []
    for rango in rangos:
        es_nuevo = True
        for rango_existente in rangos_unicos:
            if abs(rango[0] - rango_existente[0]) < 0.5 and abs(rango[1] - rango_existente[1]) < 0.5:
                es_nuevo = False
                break
        if es_nuevo:
            rangos_unicos.append(rango)
    
    # Para funciones periódicas, ajustar el intervalo de búsqueda a un rango más pequeño
    # centrado alrededor de 0 para evitar problemas con múltiples raíces
    if es_periodica and not rangos_unicos:
        # Buscar en un rango más pequeño centrado en 0 para funciones trigonométricas
        rango_periodico = (-2*np.pi, 2*np.pi)
        puntos_periodicos = np.linspace(rango_periodico[0], rango_periodico[1], pasos)
        evaluacion_periodica = f_num(puntos_periodicos)
        
        for i in range(len(puntos_periodicos)-1):
            if (np.isfinite(evaluacion_periodica[i]) and 
                np.isfinite(evaluacion_periodica[i+1]) and 
                _cambiooo(evaluacion_periodica[i]) * _cambiooo(evaluacion_periodica[i+1]) < 0):
                rangos_unicos.append((puntos_periodicos[i], puntos_periodicos[i+1]))

    return rangos_unicos #devuelve los intervalos encontrados, los cuales se usarán para que se decida cual es la mejor raíz con la cual empezar

def _sugerencia(f_num, fprima_num,intervalo,bisecciones=5):
    #f_num: la función a evaluar
    #fprima_num: derivada de la función 
    #intervalo es la tupla (a,b) donde se sabe que hay un cambio de signo
    #bisecciones es el numero de veces que se va a biseccionar para refinar
    a,b = intervalo #extrae los límites del intervalo
    fa, fb = f_num(a), f_num(b) #evaluara la función en los extremos
    punto_inicial = 0.5 * (a+b) #) es la primera aproximación al punto inicial x0 = 0.5 * (a+b)
    
    for bi in range (bisecciones): #Se recorre estableciendo como rango el parámetro pasos_bis_ini el cual controla las veces que se repertirá el refinamiento
        m = 0.5 * (a+b) #calcula el punto medio
        fm = f_num(m) #evalua la funcion
        
        if _cambiooo(fa) * _cambiooo(fm) <=0: # se decide el subintervalo si f(a) y f(m) tienen signos opuestos la raíz está en [a,m]
            b, fb = m, fm
        elif _cambiooo(fb) * _cambiooo(fm) <=0: #Si no: la raíz está en [m, b]
            a, fa = m, fm
        punto_inicial = m #se actualiza el valor del x0 está dando un mejor valor
    
    explicacion = (
        f"Sugerencia de x0 en el intervalo {intervalo}: "
        f"Se tomó el punto medio y {bisecciones} veces de bisección "
        f"para asegurar el mejor punto x0≈{punto_inicial:.6f}, f(x0)≈{f_num(punto_inicial):.3e}, "
        f"|f'(x0)|≈{abs(fprima_num(punto_inicial)):.3e}."
    )
    return punto_inicial, (a,b),explicacion

#APENAS AQUÍ SE VA A HACER EL METODO
#Se realizará mediante el safeguard Newton Method es decir que no aplicará a lo wey cada iteración sino que usará un mecanismos para evitar fallas en el método
#La manera en que se hará es combinar Newton con bisección si la iteración da un valor razonable (dentro de intervalo) se va usar
#Si se sale del intervalo o la derivada es chica se recurre a bisección, garantiza que la raíz esté en el subintervalo

def Newton(f_num, fprima_num, f_str,intervalo: Tuple[float, float],tolerancia_x=1e-8, tolerancia_f=1e-10, limite=50,bisecciones=5,mostrar_tangentes=True, es_periodica=False):
#f_num evalua cada iteración para xn
#fprima_num derivada de la función útil para el método
#f_str representará la funcióm para display
#intervalo tupla de dos floats, es el intervalo donde se busca la raíz
#tolerancia_x por defecto asigan 1e-8 ayudara a identificar cuando la diferencia entre iteraciones es poca
#tolerancia_f por defecto es 1e-10, es la tolerancia en el valor de la funcióm. es decir lo que verifica que f(x) está muy cerca de 0
#limite define el limite de iteraciones, maximo asigné 50
#bisecciones numero de veces que hace bisección, ayudará a alejar puntos donde la derivada es casi igual a 0 lo que mejora la convergenica
#mostrar tangentes por defecto true controla si se deben de visualizar las tangentes
#es_periodica indica si es función trigonométrica para ajustar las gráficas
    punto_inicial, (a,b), x0 = _sugerencia(f_num,fprima_num, intervalo,bisecciones)
    
    pasos: List[movida] = []
    xn = punto_inicial
    
    print('\n----- SUGERENCIA DE PUNTO INICIAL -----')
    print(x0)
    
    print('\n----- ITERACIONES -----')
    print("{:>2} {:>3} {:>18} {:>14} {:>14} {:>14} {:>14} descripcion".format(
    'n', 'met', 'x_n', 'f(x_n)', 'f\'(x_n)', 'Δ', 'error'))

    for n in range (1, limite+1):
        fn = float(f_num(xn))
        fpn = float(fprima_num(xn))
        metodo = ""
        descripcion = ""
        delta = None
        nuevo_x = None
        
        if np.isfinite(fpn) and abs(fpn) > 1e-12:
            delta = -fn / fpn
            opcion = xn + delta
            if a < opcion < b and np.isfinite(opcion):
                metodo = "NR"
                nuevo_x = opcion
                descripcion = _formato_descripcion(xn,fn,fpn,nuevo_x)
            else:
                metodo = "BIS"
                nuevo_x = 0.5 * (a+b)
                descripcion = "Con Newton se salió del intervalo se pasa a bisección"
        else: 
            metodo = "BIS"
            nuevo_x = 0.5 * (a+b)
            descripcion = "Con Newton se salió del intervalo se pasa a bisección"
            
        nueva_fx = float(f_num(nuevo_x))
        if _cambiooo(f_num(a)) * _cambiooo(nueva_fx) <= 0:
            b = nuevo_x
        else:
            a = nuevo_x
            
        error = abs(nuevo_x - xn)
        pasos.append(movida(n,metodo,nuevo_x,nueva_fx,None if metodo=="BIS" else fpn,delta,error,descripcion))
        
        fprimax_mensaje = f"{fpn:14.10f}" if metodo == "NR" else " "*14
        delta_mensaje = f"{delta:14.10f}" if metodo == "NR" and delta is not None else " "*14
        print(f"{n:>2}{metodo:>3} {nuevo_x:>18.10f}{nueva_fx:>14.10f}{fprimax_mensaje}{delta_mensaje}{error:>14.10f} {descripcion}")

        if abs(nueva_fx) < tolerancia_f:
            print(f"→ Paro por residuo |f(x)|<{tolerancia_f}")
            xn = nuevo_x
            break
        if error < tolerancia_x:
            print(f"→ Paro por error |Δx|<{tolerancia_x}")
            xn = nuevo_x
            break   
        
        xn = nuevo_x
        
        # === Gráficas ===
        xs = [p.x for p in pasos]

        # --- Ajustar rangos según si es función periódica o no
        if es_periodica:
            # Para funciones periódicas: mostrar varios periodos alrededor del intervalo
            a_glob, b_glob = intervalo
            margen_global = 2 * np.pi  # Mostrar 2π adicionales en cada lado
            gx_glob = np.linspace(a_glob - margen_global, b_glob + margen_global, 1000)
            
            # Zoom: centrado en las iteraciones con margen de π
            xmin, xmax = min(xs + [a]), max(xs + [b])
            margen_zoom = np.pi  # Margen de π para ver bien la periodicidad
            gx_zoom = np.linspace(xmin - margen_zoom, xmax + margen_zoom, 800)
        else:
            # --- Rango GLOBAL (centrado en el intervalo detectado)
            a_glob, b_glob = intervalo
            margen_global = 0.2 * (b_glob - a_glob) + 10
            gx_glob = np.linspace(a_glob - margen_global, b_glob + margen_global, 800)
            
            # --- Rango ZOOM (muy cerca de las iteraciones)
            xmin, xmax = min(xs + [a]), max(xs + [b])
            margen_zoom = 0.1 * (xmax - xmin + 1e-12)
            gx_zoom = np.linspace(xmin - margen_zoom, xmax + margen_zoom, 800)

        gy_glob = f_num(gx_glob)
        gy_zoom = f_num(gx_zoom)

        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # ----- Panel GLOBAL -----
        ax = axes[0]
        ax.axhline(0, color="red", linewidth=1)
        ax.plot(gx_glob, gy_glob, label=f"f(x)={f_str}", linewidth=2)
        ax.plot([a_glob, b_glob], [f_num(a_glob), f_num(b_glob)], 'o', 
                markersize=8, label="Extremos del intervalo")

        # marcar iteraciones
        for i, p in enumerate(pasos, start=1):
            ax.plot(p.x, p.fx, 'o', markersize=6)
            ax.text(p.x, p.fx, f"{p.metodo}{i}", fontsize=8, 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))

        ax.set_title("Vista GLOBAL" + (" (Función Periódica)" if es_periodica else ""))
        ax.set_xlabel("x"); ax.set_ylabel("f(x)")
        ax.grid(True, alpha=0.3); ax.legend()
        
        # Formatear eje x con valores de π si es función periódica
        if es_periodica:
            _formatear_eje_pi(ax, gx_glob[0], gx_glob[-1])

        # ----- Panel ZOOM -----
        ax = axes[1]
        ax.axhline(0, color="black", linewidth=1)
        ax.plot(gx_zoom, gy_zoom, label=f"f(x)={f_str}", linewidth=2)

        for i, p in enumerate(pasos, start=1):
            ax.plot(p.x, p.fx, 'o', color="red", markersize=8)
            ax.text(p.x, p.fx, f"{p.metodo}{i}", fontsize=10, 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))

        if mostrar_tangentes:
            for p in pasos[:5]:  # Muestra solo las primeras 5 tangenntes
                if p.metodo == "NR" and p.f_prima_x is not None: 
                    t = np.linspace(p.x - (xmax-xmin)*0.5, p.x + (xmax-xmin)*0.5, 50)
                    y_tan = p.fx + p.f_prima_x * (t - p.x)
                    ax.plot(t, y_tan, "--", linewidth=1.5, alpha=0.8, 
                           label=f"Tangente {p.n}" if p.n == 1 else "")

        ax.set_title("Vista ZOOM (cerca de la raíz)" + (" - Periódica" if es_periodica else ""))
        ax.set_xlabel("x"); ax.set_ylabel("f(x)")
        ax.grid(True, alpha=0.3); ax.legend()
        
        # Formatear eje x con valores de π si es función periódica
        if es_periodica:
            _formatear_eje_pi(ax, gx_zoom[0], gx_zoom[-1])

        plt.suptitle("Newton–Raphson" + (" - Función Periódica" if es_periodica else ""), fontsize=14)
        plt.tight_layout()
        plt.show()

        return pasos[-1].x, pasos
    
    return xn, pasos

def newton_protegido(
    funcion_string: str,
    rango_busqueda: Tuple[float, float] = (-100, 100),
    tolerancia_x=1e-8, tolerancia_f=1e-10,
    limite=50, bisecciones=5
):
    x = sp.symbols('x')
    f_sym = sp.sympify(funcion_string)
    fp_sym = sp.diff(f_sym, x)
    f_num = sp.lambdify(x, f_sym, "numpy")
    fp_num = sp.lambdify(x, fp_sym, "numpy")
    
    # Detectar si es función periódica
    es_periodica = _es_funcion_periodica(funcion_string)
    
    # Si es función periódica, ajustar el rango de búsqueda a un rango más pequeño
    if es_periodica:
        print("Función periódica detectada. Ajustando búsqueda a [-2π, 2π] para usar radianes.")
        rango_busqueda = (-2*np.pi, 2*np.pi)

    intervalos = encontrar_intervalos(f_num, intervalo=rango_busqueda, pasos=2000, es_periodica=es_periodica)
    if not intervalos:
        print("No se detectaron raíces en el rango.")
        return [], []

    todas_raices = []
    historiales = []

    for intervalo in intervalos:
        raiz, pasos = Newton(f_num, fp_num, funcion_string, intervalo, tolerancia_x, tolerancia_f, 
                           limite, bisecciones, mostrar_tangentes=True, es_periodica=es_periodica)
        todas_raices.append(raiz)
        historiales.append(pasos)

    return todas_raices, historiales
