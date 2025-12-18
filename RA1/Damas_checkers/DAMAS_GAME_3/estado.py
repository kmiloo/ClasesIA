import copy

class Estado:
    def __init__(self, board, current_player):
        self.board = board
        self.current_player = current_player

    def get_valid_moves(self):
        return self.board.get_valid_moves(self.current_player)

    def move(self, move):
        new_board = copy.deepcopy(self.board)
        start, end = move
        new_board.move_piece(start, end)
        next_player = 'b' if self.current_player == 'w' else 'w'
        return Estado(new_board, next_player)

    def is_terminal(self):
        return self.board.game_over()

    def heuristica(self, max_jugador, min_jugador):
        puntos = 0
        for fila in self.board.board:
            for celda in fila:
                if celda == max_jugador:
                    puntos += 1 
                elif celda == min_jugador:
                    puntos -= 1 
                elif celda == max_jugador.upper():  
                    puntos += 4 
                elif celda == min_jugador.upper(): 
                    puntos -= 4 
        return puntos

