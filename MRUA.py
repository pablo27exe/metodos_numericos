#EXAMEN PRIMER PARCIAL PABLO ANGEL MUNGUÍA ROMERO ID22028 :)
#La congigurción inicial la dejé en 0, no es necesario modificarla ya que hay controles en el gráfico para manipularlos


import numpy as np #Librería para realizar los cálculos
import matplotlib.pyplot as plt #librería para gráfico
from matplotlib.widgets import Slider #importa la clase slider del modulo del widgets (se va usar para poder controlar los valores en tiempo real)

# Configuración inicial
x0_initial = 0.0 #valor inicial de la posición
v0_initial = 0.0 #valor inicial de la velocidad
a_initial = 0.0 #valor inicial de la aceleración
t = np.linspace(0, 10, 100) #se crea un arreglo de 100 valores espaciados entre 0 y 10, 0: tiempo inicial, 10: tiempo final, 100: puntos en el intervalo (LOS GRAFICOS SOLO MOSTRARÁN HASTA 10 SEGUNDOS)

# Crear figura y subplots
graficos, (grafico_aceleracion, grafico_velocidad) = plt.subplots(1, 2, figsize=(15, 8))
#fig diseña la página donde se mostrará todo
#grafico_aceleracion primer subgrafico (el de aceleración)
#grafico_velocidad para la velocidad
#1, 2 (1 fila y dos columnas) 
#tamaño de 15 x 8 pulgadas
plt.subplots_adjust(bottom=0.3)#margen de 30% para que los slides no se sobrepongan a los gráficos

# Calcular valores Función para el cálculo de los sistemas generales
def calCulo(x0, v0, a): #recibe los valores de posición, velocidad y aceleración
    v = v0 + a * t #calculo de la velocidad en cada instante del tiempo (Velocidad final = Velocidad inicial + aceleración × tiempo)
    x = x0 + v0 * t + 0.5 * a * t**2 #calculo de la aceleración en cada instante del tiempo (Posición = Posición inicial + velocidad inicial × tiempo + mitad de aceleración × tiempo al cuadrado)
    return x, v #devuelve las posiciones y velocidades calculadas

x_initial, v_initial = calCulo(x0_initial, v0_initial, a_initial) #llama a la función con los valores iniciales y guarda los resultado en variables, de modo que calcula automáticamente la posición para cualquier conjunto de parámetros fisicos.

# Graficar datos iniciales
linea_de_aceleracion, = grafico_aceleracion.plot(t, x_initial, 'g-', linewidth=2)
#t: eje x (tiempo), x_initial: eje Y  (posición), de color verde con grosor de 2px
linea_de_velocidad, = grafico_velocidad.plot(t, v_initial, 'g-', linewidth=2)
#t: eje x (tiempo), v_initial: eje Y (velocidad) de color verde con grosor de 2px

#diseño de los ejes
grafico_aceleracion.set_xlabel('Tiempo (s)')#eje x
grafico_aceleracion.set_ylabel('Posición (m)')#eje y
grafico_aceleracion.set_title('Aceleración(x = x₀ + v₀ · t + ½ · a · t²)') #titulo del gráfcio
grafico_aceleracion.grid(True, alpha=0.5) #cuadricula con transparencia de 0.5
grafico_aceleracion.axhline(y=0, color='k', linestyle='--', alpha=0.5) #línea horizontal para y = 0 ayuda a indicar el origen

grafico_velocidad.set_xlabel('Tiempo (s)')#eje x
grafico_velocidad.set_ylabel('Velocidad (m/s)')#eje y
grafico_velocidad.set_title('Velocidad (v = v₀ + a · t)')#titulo del gráfcio
grafico_velocidad.grid(True, alpha=0.5) #cuadricula con transparencia de 0.5
grafico_velocidad.axhline(y=0, color='k', linestyle='--', alpha=0.5) #línea horizontal para y = 0 ayuda a indicar el origen

# Sliders
ax_x0 = plt.axes([0.2, 0.15, 0.6, 0.03])
ax_v0 = plt.axes([0.2, 0.10, 0.6, 0.03])
ax_a = plt.axes([0.2, 0.05, 0.6, 0.03])
#para los slider se crea un área con las siguientes medidas
#20 % lado izquierdo
#15, 10 y 5% abajo
#60% de ancho
#3% de alto

slider_x0 = Slider(ax_x0, 'Posición Inicial (x0)', -50.0, 50.0, valinit=x0_initial)
slider_v0 = Slider(ax_v0, 'Velocidad Inicial (v0)', -50.0, 50.0, valinit=v0_initial)
slider_a = Slider(ax_a, 'Aceleración (a)', -50.0, 50.0, valinit=a_initial)
#se crean los sliders
#ax_x0, ax_v0 y ax_a define la posición donde van a estar, una etiqueta para explicar que controla cada uno, y un rango de valores de -50 a 50

# Formatear números (mejorará la manera de ver las ecuaciones)
def formato(valor): #recibirá un valor númerico
    if valor >= 0:
        return f"+ {abs(valor):.2f}" #si es mayor a 0 devulve el numero con el signo + y su valor abosluto con dos decimales
    else:
        return f"- {abs(valor):.2f}" #si es negativo devulve el numero con el signo - y su valor abosluto con dos decimales

# Función para actualizar los valores (permitirá que la visualización en tiempo real funciones)
def actualizacion(val):
    x0 = slider_x0.val #obtiene el valor del slider de la posición
    v0 = slider_v0.val #obtiene el valor del slider de la velocidad
    a = slider_a.val #obtiene el valor del slider de la aceleración
    
    x, v = calCulo(x0, v0, a) #llama a caluclar valores con los valores obtenidos del slider y los calcula
    
    linea_de_aceleracion.set_ydata(x)#actualiza los datos del eje Y, lo que hace que el cambio se vea reflejado en la linea del gráfico, los valores son reemplazados con los nuevos calculados, pero manntiene el tiempo.
    linea_de_velocidad.set_ydata(v)
    
    # Actualizar ecuaciones en las leyendas
    ecuacion_aceleracion = f'$x(t) = {x0:.2f} {formato(v0)}t {formato(0.5*a)}t^{{2}}$'
    ecuacion_velocidad = f'$v(t) = {v0:.2f} {formato(a)}t$'
    
    #ambos casos crean una cadena de texto con las ecuaciones formateadas
    #hacen uso de la notación $...$ LaTeX para formato matemático
    #irá cambiando el valor de x0, v0 y a al ir deslizando 
    
    # Actualizar leyendas 
    leyenda_aceleracion.get_texts()[0].set_text(ecuacion_aceleracion)
    leyenda_velocidad.get_texts()[0].set_text(ecuacion_velocidad)
    #las cadenas previamente actualizadas harán que el texto de la gráfica se cambie
    
    # Ajustar límites automáticamente
    grafico_aceleracion.relim() #Determinar los nuevos valores mínimo y máximo de los datos después de la actualización.
    grafico_aceleracion.autoscale_view() #Ajusta automáticamente la escala del eje Y 
    grafico_velocidad.relim()
    grafico_velocidad.autoscale_view()
    
    graficos.canvas.draw_idle()#hasta este momento hace el redibujo de la gráfica tomando los nuevo datos

# Inicializar leyendas con ecuaciones iniciales
ecuacion_aceleracion_inicial = f'$x(t) = {x0_initial:.2f} {formato(v0_initial)}t {formato(0.5*a_initial)}t^{{2}}$' #crea la ecuación de aceleración inicial 
ecuacion_velocidad_inicial = f'$v(t) = {v0_initial:.2f} {formato(a_initial)}t$'#crea la ecuación de velocidad inicial 

leyenda_aceleracion = grafico_aceleracion.legend([linea_de_aceleracion], [ecuacion_aceleracion_inicial], loc='lower left', fontsize=10)

leyenda_velocidad = grafico_velocidad.legend([linea_de_velocidad], [ecuacion_velocidad_inicial], loc='lower left', fontsize=10)

#crea la leyenda para el grafico
#linea_de_aceleracion, linea_de_velocidad son las líneas que representan cada ecucación
#texto de la ecuación
#posicion en la equina inferior izquierda y tamaño de fuente de 10

# Conectar sliders a los valores
slider_x0.on_changed(actualizacion)
slider_v0.on_changed(actualizacion)
slider_a.on_changed(actualizacion)
#se llama a la función de actualizar valores para que los valores de los slider afecten al grafico

plt.show()#muestra el gráfico
