from board import Board
from move import Move

class Game:
    def __init__(self):
        self.board = Board()
        self.turn = Board.BLACK  # Black starts first
        self.valid_moves = {}
        self.selected = None
        self.game_over = False
        self.winner = None

    def reset(self):
        self.__init__()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
            
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(self.selected.row, self.selected.col)
        if piece and (row, col) in self.valid_moves:
            move = Move(piece.row, piece.col, row, col, self.valid_moves[(row, col)])
            self.board.move(piece, move)
            skipped = move.captured_pieces
            if skipped:
                self.valid_moves = self.board.get_valid_moves(piece)
                if self.valid_moves:
                    return True
            
            self.change_turn()
            return True
        return False

    def change_turn(self):
        self.valid_moves = {}
        self.selected = None
        self.turn = Board.BLACK if self.turn == Board.WHITE else Board.WHITE
        self.check_winner()

    def check_winner(self):
        winner = self.board.winner()
        if winner:
            self.game_over = True
            self.winner = winner

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()