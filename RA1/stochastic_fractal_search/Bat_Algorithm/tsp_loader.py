import numpy as np

def load_tsp_file(filename):
    """Carga un archivo TSP y devuelve las coordenadas de las ciudades"""
    cities = []
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    read_data = False
    for line in lines:
        if "NODE_COORD_SECTION" in line:
            read_data = True
            continue
        if "EOF" in line:
            break
        if read_data:
            parts = line.strip().split()
            cities.append([float(parts[1]), float(parts[2])])
    
    return np.array(cities)

def calculate_distance_matrix(cities):
    """Calcula la matriz de distancias entre ciudades"""
    n = len(cities)
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            matrix[i][j] = np.linalg.norm(cities[i] - cities[j])
    return matrix