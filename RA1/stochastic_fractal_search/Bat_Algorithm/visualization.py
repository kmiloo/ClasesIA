import matplotlib.pyplot as plt
import numpy as np

def plot_route(cities, route, distance):
    """Visualiza la mejor ruta encontrada"""
    plt.figure(figsize=(12, 6))
    
    ordered_cities = cities[route]
    ordered_cities = np.vstack((ordered_cities, ordered_cities[0]))
    
    plt.scatter(cities[:, 0], cities[:, 1], c='red', s=50)
    plt.plot(ordered_cities[:, 0], ordered_cities[:, 1], 'b-')
    
    for i, city in enumerate(cities):
        plt.text(city[0], city[1], str(i), fontsize=8)
    
    plt.title(f"Mejor ruta encontrada - Distancia: {distance:.2f}")
    plt.xlabel("Coordenada X")
    plt.ylabel("Coordenada Y")
    plt.grid(True)
    plt.show()

def plot_convergence(fitness_history):
    """Muestra la convergencia del algoritmo"""
    plt.figure(figsize=(12, 6))
    plt.plot(fitness_history, 'r-')
    plt.title("Convergencia del Bat Algorithm")
    plt.xlabel("Iteración")
    plt.ylabel("Distancia")
    plt.grid(True)
    plt.show()