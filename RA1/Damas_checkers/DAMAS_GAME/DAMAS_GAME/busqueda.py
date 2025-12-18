import math
from estado import Estado

class Busqueda:
    def __init__(self, tablero, jugador_max, jugador_min):
        self.tablero = tablero
        self.jugador_max = jugador_max  
        self.jugador_min = jugador_min  
        self.estados_descubiertos = 0

    def minimax(self, estado, profundidad, alpha, beta, jugador_maximizador):
        if profundidad == 0 or estado.es_terminal():
            return estado.heuristica(self.jugador_max, self.jugador_min) 

        if jugador_maximizador: 
            max_eval = -math.inf
            for movimiento in estado.obtener_movimientos_validos():  
                nuevo_estado = estado.mover(movimiento) 
                eval = self.minimax(nuevo_estado, profundidad - 1, alpha, beta, False)  
                max_eval = max(max_eval, eval) 
                alpha = max(alpha, eval) 
                if beta <= alpha: 
                    break
            return max_eval
        else:  
            min_eval = math.inf
            for movimiento in estado.obtener_movimientos_validos(): 
                nuevo_estado = estado.mover(movimiento)  
                eval = self.minimax(nuevo_estado, profundidad - 1, alpha, beta, True) 
                min_eval = min(min_eval, eval) 
                beta = min(beta, eval) 
                if beta <= alpha: 
                    break
            return min_eval