import math
from estado import Estado

class Busqueda:
    def __init__(self, board, max_player, min_player):
        self.board = board
        self.max_player = max_player  
        self.min_player = min_player  
        self.estados_descubiertos = 0

    def minimax(self, estado, depth, alpha, beta, maximizing_player):
        if depth == 0 or estado.is_terminal():
            return estado.heuristica(self.max_player, self.min_player) 

        if maximizing_player: 
            max_eval = -math.inf
            for move in estado.get_valid_moves():  
                new_state = estado.move(move) 
                eval = self.minimax(new_state, depth - 1, alpha, beta, False)  
                max_eval = max(max_eval, eval) 
                alpha = max(alpha, eval) 
                if beta <= alpha: 
                    break
            return max_eval
        else:  
            min_eval = math.inf
            for move in estado.get_valid_moves(): 
                new_state = estado.move(move)  
                eval = self.minimax(new_state, depth - 1, alpha, beta, True) 
                min_eval = min(min_eval, eval) 
                beta = min(beta, eval) 
                if beta <= alpha: 
                    break
            return min_eval