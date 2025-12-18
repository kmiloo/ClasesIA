import numpy as np

class BatAlgorithmTSP:
    def __init__(self, distance_matrix, n_bats=20, iterations=100, 
                 freq_min=0, freq_max=1, loudness=0.5, pulse_rate=0.5):
        self.dist_matrix = distance_matrix
        self.n_bats = n_bats
        self.iterations = iterations
        self.freq_min = freq_min
        self.freq_max = freq_max
        self.A = loudness
        self.r = pulse_rate
        
        self.n_cities = distance_matrix.shape[0]
        self.bats = [np.random.permutation(self.n_cities) for _ in range(n_bats)]
        self.velocities = [np.zeros(self.n_cities, dtype=int) for _ in range(n_bats)]
        self.fitness = self.calculate_fitness(self.bats)
        self.best_bat = self.bats[np.argmin(self.fitness)]
        self.best_fitness = min(self.fitness)
        
    def calculate_fitness(self, population):
        """Calcula la distancia total para cada murciélago"""
        return [self.tour_distance(bat) for bat in population]
    
    def tour_distance(self, route):
        """Calcula la distancia total de una ruta"""
        return sum(self.dist_matrix[route[i], route[(i+1) % self.n_cities]] 
                   for i in range(self.n_cities))
    
    def mutate(self, route):
        """Operador de mutación: intercambio de dos ciudades"""
        new_route = route.copy()
        i, j = np.random.choice(self.n_cities, 2, replace=False)
        new_route[i], new_route[j] = new_route[j], new_route[i]
        return new_route
    
    def run(self):
        """Ejecuta el algoritmo"""
        fitness_history = []
        
        for _ in range(self.iterations):
            for i in range(self.n_bats):
                freq = self.freq_min + (self.freq_max - self.freq_min) * np.random.rand()
                
                # Generar nueva solución
                new_solution = self.bats[i].copy()
                for _ in range(int(freq * self.n_cities)):
                    new_solution = self.mutate(new_solution)
                
                # Aplicar búsqueda local
                if np.random.rand() > self.r:
                    new_solution = self.mutate(self.best_bat)
                
                # Evaluar nueva solución
                new_fitness = self.tour_distance(new_solution)
                
                # Actualizar si es mejor
                if new_fitness < self.fitness[i] and np.random.rand() < self.A:
                    self.bats[i] = new_solution
                    self.fitness[i] = new_fitness
                    
                    if new_fitness < self.best_fitness:
                        self.best_bat = new_solution
                        self.best_fitness = new_fitness
            
            fitness_history.append(self.best_fitness)
        
        return self.best_bat, self.best_fitness, fitness_history