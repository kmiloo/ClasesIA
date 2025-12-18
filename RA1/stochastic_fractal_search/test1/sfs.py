import numpy as np

def sfs(objective_func, dim, pop_size, max_iter, lb, ub):
    # Inicialización
    population = np.random.uniform(lb, ub, (pop_size, dim))
    fitness = np.array([objective_func(ind) for ind in population])
    best_idx = np.argmin(fitness)
    best_solution, best_fitness = population[best_idx].copy(), fitness[best_idx]
    
    for iter in range(max_iter):
        # Fase de Difusión (Exploración)
        for i in range(pop_size):
            epsilon = np.random.normal(0, 1)  # Gaussiano
            j = np.random.choice([k for k in range(pop_size) if k != i])
            new_solution = population[i] + epsilon * (population[j] - population[i])
            new_solution = np.clip(new_solution, lb, ub)
            new_fitness = objective_func(new_solution)
            
            if new_fitness < fitness[i]:
                population[i], fitness[i] = new_solution, new_fitness
                if new_fitness < best_fitness:
                    best_solution, best_fitness = new_solution.copy(), new_fitness
        
        # Fase de Actualización (Explotación)
        for i in range(pop_size):
            if np.random.rand() < 0.5:  # Probabilidad de actualización
                perturbation = np.random.normal(0, 0.1, dim)  # Pequeña perturbación
                new_solution = population[i] + perturbation
                new_solution = np.clip(new_solution, lb, ub)
                new_fitness = objective_func(new_solution)
                
                if new_fitness < fitness[i]:
                    population[i], fitness[i] = new_solution, new_fitness
    
    return best_solution, best_fitness