import copy

class Estado:
    def __init__(self, tablero, jugador_actual):
        self.tablero = tablero
        self.jugador_actual = jugador_actual

    def obtener_movimientos_validos(self):
        return self.tablero.obtener_movimientos_validos(self.jugador_actual)

    def mover(self, movimiento):
        nuevo_tablero = copy.deepcopy(self.tablero)
        inicio, fin = movimiento
        nuevo_tablero.mover_pieza(inicio, fin)
        siguiente_jugador = 'b' if self.jugador_actual == 'w' else 'w'
        return Estado(nuevo_tablero, siguiente_jugador)

    def es_terminal(self):
        return self.tablero.fin_juego()

    def heuristica(self, jugador_max, jugador_min):
        puntos = 0
        for fila in self.tablero.tablero:
            for celda in fila:
                if celda == jugador_max:
                    puntos += 1 
                elif celda == jugador_min:
                    puntos -= 1 
                elif celda == jugador_max.upper():  
                    puntos += 4 
                elif celda == jugador_min.upper(): 
                    puntos -= 4 
        return puntos
