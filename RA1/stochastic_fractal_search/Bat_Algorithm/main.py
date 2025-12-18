from tsp_loader import load_tsp_file, calculate_distance_matrix
from bat_algorithm import BatAlgorithmTSP
from visualization import plot_route, plot_convergence

# Cargar datos
filename = "berlin52.tsp"  # Descargar de TSPLIB y poner en el directorio
cities = load_tsp_file(filename)
distance_matrix = calculate_distance_matrix(cities)

# Parámetros del algoritmo
params = {
    "distance_matrix": distance_matrix,
    "n_bats": 50,
    "iterations": 500,
    "freq_min": 0,
    "freq_max": 1,
    "loudness": 0.5,
    "pulse_rate": 0.5
}

# Ejecutar algoritmo
ba = BatAlgorithmTSP(**params)
best_route, best_distance, fitness_history = ba.run()

# Resultados
print(f"\nMejor distancia encontrada: {best_distance}")
print(f"Ruta óptima: {best_route}")

# Visualización
plot_route(cities, best_route, best_distance)
plot_convergence(fitness_history)