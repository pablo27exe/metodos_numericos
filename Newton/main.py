from newton_raphson import (
 newton_protegido
)

funcion = input("Ingrese la función: ")

raices, historiales = newton_protegido(
        funcion_string = funcion,
        rango_busqueda=(0,120),
        tolerancia_x=1e-6,tolerancia_f=1e-12,
        limite=50, bisecciones=5
    )