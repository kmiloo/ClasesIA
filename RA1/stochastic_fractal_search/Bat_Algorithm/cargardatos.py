import numpy as np

def leer_tsp(archivo):
    ciudades = []
    with open(archivo, 'r') as f:
        lineas = f.readlines()
    leer_datos = False
    for linea in lineas:
        if "NODE_COORD_SECTION" in linea:
            leer_datos = True
            continue
        if "EOF" in linea:
            break
        if leer_datos:
            partes = linea.strip().split()
            ciudades.append([float(partes[1]), float(partes[2])])
    return np.array(ciudades)

#ciudades = leer_tsp("berlin52.tsp")