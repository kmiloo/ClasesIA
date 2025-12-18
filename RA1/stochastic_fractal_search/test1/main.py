from sfs import *


def sphere(x):
    return sum(x**2)

dimensión = 3
población = 30
iteraciones = 100

mejor_solución = stochastic_fractal_search(sphere, dimensión, población, iteraciones)
print("Mejor solución:", mejor_solución)