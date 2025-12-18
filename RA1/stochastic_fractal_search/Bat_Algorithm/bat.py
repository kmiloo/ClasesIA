import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button  # Nueva importación
from mpl_toolkits.mplot3d import Axes3D


def ackley(x):
    x = np.array(x)
    a = 20
    b = 0.2
    c = 2 * np.pi
    sum_sq = np.sum(x**2)
    sum_cos = np.sum(np.cos(c * x))
    n = len(x)
    return -a * np.exp(-b * np.sqrt(sum_sq/n)) - np.exp(sum_cos/n) + a + np.e


class VisualBatAlgorithm:
    def __init__(self, n_bats=50, iterations=200, freq_range=(0, 2), A=0.9, r=0.7):
        self.n_bats = n_bats
        self.iterations = iterations
        self.freq_min, self.freq_max = freq_range
        self.A = A
        self.r = r
        self.anim = None
        self.historical_best = []
        
        # Inicialización de murciélagos
        self.bats = np.random.uniform(-5, 5, (n_bats, 2))
        self.velocities = np.zeros((n_bats, 2))
        self.fitness = np.array([ackley(bat) for bat in self.bats])
        self.best_bat = self.bats[np.argmin(self.fitness)]
        self.best_fitness = self.fitness.min()
        
        # Configurar gráficos
        self.fig = plt.figure(figsize=(18, 8))
        
        # Añadir espacio para el botón
        self.fig.subplots_adjust(bottom=0.2)
        
        # Crear subplots
        self.ax3d = self.fig.add_subplot(131, projection='3d')
        self.ax2d = self.fig.add_subplot(132)
        self.ax_conv = self.fig.add_subplot(133)
        
        # Botón de inicio
        self.ax_button = plt.axes([0.4, 0.05, 0.2, 0.075])  # Posición [left, bottom, width, height]
        self.start_button = Button(self.ax_button, 'INICIAR')
        self.start_button.on_clicked(self.start_animation)
        
        # Precalcular superficie 3D
        x = y = np.linspace(-5, 5, 50)
        X, Y = np.meshgrid(x, y)
        Z = np.array([[ackley([xi, yi]) for xi, yi in zip(row_x, row_y)] 
                     for row_x, row_y in zip(X, Y)])
        self.ax3d.plot_surface(X, Y, Z, cmap='viridis', alpha=0.6)
        self.scat3d = self.ax3d.scatter([], [], [], c='red', s=50)
        
        # Configurar gráfico 2D
        self.contour = self.ax2d.contourf(X, Y, Z, levels=20, cmap='viridis')
        self.scat2d = self.ax2d.scatter([], [], c='white', s=50, alpha=0.6)
        self.quiver = self.ax2d.quiver(
            self.bats[:,0],
            self.bats[:,1],
            self.velocities[:,0],
            self.velocities[:,1],
            color='white', 
            scale=20
        )
        
        # Configurar gráfico de convergencia
        self.conv_line, = self.ax_conv.plot([], [], 'r-')
        self.ax_conv.set_xlim(0, iterations)
        self.ax_conv.set_ylim(0, 20)

    def update(self, frame):
        # Lógica de actualización igual que antes
        for i in range(self.n_bats):
            # se genera una frecuencia aleatoria para el murciélago
            freq = self.freq_min + (self.freq_max - self.freq_min) * np.random.rand()
            # se actualiza la velocidad del murciélago
            self.velocities[i] += (self.bats[i] - self.best_bat) * freq
            # se actualiza la posición del murciélago segun la posción y la velocidad
            new_bat = self.bats[i] + self.velocities[i]
            # se hace una búsqueda local cerca de la mejor solución 
            # lo que permite explotar alrededor de la mejor solución conocida
            if np.random.rand() > self.r:
                new_bat = self.best_bat + 0.5 * np.random.randn(2)
            
            # se evalúa la calidad de la nueva solución con la función objetivo
            new_fitness = ackley(new_bat)
            
            # si es mejor que la anterior.
            # y con una probabilidad dada por la sonoridad 
            # lo cual introduce aleatoriedad controlada.
            if new_fitness < self.fitness[i] and np.random.rand() < self.A:
                self.bats[i] = new_bat
                self.fitness[i] = new_fitness
                # si esta solución es mejor que la global, se actualiza self.best_bat y su fitness.
                if new_fitness < self.best_fitness:
                    self.best_bat = new_bat
                    self.best_fitness = new_fitness
        
        # Actualizar gráficos
        self.scat3d._offsets3d = (self.bats[:,0], self.bats[:,1], [ackley(b) for b in self.bats])
        self.scat2d.set_offsets(self.bats)
        self.scat2d.set_array(self.fitness)
        self.quiver.set_offsets(self.bats)
        self.quiver.set_UVC(self.velocities[:,0], self.velocities[:,1])
        
        # Actualizar convergencia
        self.historical_best.append(self.best_fitness)
        x_data = list(range(len(self.historical_best)))
        y_data = self.historical_best
        self.conv_line.set_data(x_data, y_data)

        self.ax_conv.set_ylim(min(y_data) - 0.5, max(y_data) + 0.5)
        print(f"Iteración {frame}: Mejor solución = {self.best_fitness:.4f}")
        
        return self.scat3d, self.scat2d, self.quiver, self.conv_line

    def start_animation(self, event):
        if not self.anim:
            self.anim = FuncAnimation(
                self.fig, 
                self.update, 
                frames=self.iterations, 
                interval=100, 
                blit=True, 
                repeat=False
            )
        else:
            self.anim.event_source.start()
        
        self.start_button.set_active(False)  

    def run(self):
        plt.show()


if __name__ == "__main__":
    ba = VisualBatAlgorithm(n_bats=30, iterations=101)
    ba.run()