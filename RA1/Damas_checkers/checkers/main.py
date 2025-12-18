from testdamas.game import Game

def print_board(board):
    print(board)

def main():
    game = Game()
    
    while not game.game_over:
        print_board(game.get_board())
        print(f"Turno de {'Negras' if game.turn == game.board.BLACK else 'Blancas'}")
        
        try:
            row = int(input("Fila: "))
            col = int(input("Columna: "))
            
            if game.select(row, col):
                if game.selected:
                    print("Movimientos válidos:", game.valid_moves)
                    new_row = int(input("Nueva fila: "))
                    new_col = int(input("Nueva columna: "))
                    game.select(new_row, new_col)
        except ValueError:
            print("Entrada inválida. Intente de nuevo.")
    
    print(f"¡Juego terminado! Ganador: {'Negras' if game.winner == game.board.BLACK else 'Blancas'}")

if __name__ == "__main__":
    main()