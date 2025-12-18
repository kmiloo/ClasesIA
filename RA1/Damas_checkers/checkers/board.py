from piece import Piece
from move import Move

class Board:
    ROWS = COLS = 8
    WHITE = 'white'
    BLACK = 'black'

    def __init__(self):
        self.board = []
        self.white_left = self.black_left = 12
        self.white_kings = self.black_kings = 0
        self.create_board()

    def create_board(self):
        for row in range(self.ROWS):
            self.board.append([])
            for col in range(self.COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(self.BLACK, row, col))
                    elif row > 4:
                        self.board[row].append(Piece(self.WHITE, row, col))
                    else:
                        self.board[row].append(None)
                else:
                    self.board[row].append(None)

    def move(self, piece, move):
        self.board[piece.row][piece.col], self.board[move.end_row][move.end_col] = None, piece
        piece.row, piece.col = move.end_row, move.end_col
        
        if move.captured_pieces:
            for captured in move.captured_pieces:
                self.remove(captured)

        # Check if piece becomes king
        if (piece.color == self.WHITE and piece.row == 0) or (piece.color == self.BLACK and piece.row == self.ROWS - 1):
            piece.make_king()
            if piece.color == self.WHITE:
                self.white_kings += 1
            else:
                self.black_kings += 1

    def remove(self, piece):
        if piece is None:
            return
        self.board[piece.row][piece.col] = None
        if piece.color == self.WHITE:
            self.white_left -= 1
        else:
            self.black_left -= 1

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == self.BLACK or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, self.ROWS), piece.direction, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, self.ROWS), piece.direction, piece.color, right))

        if piece.color == self.WHITE or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), piece.direction, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), piece.direction, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current is None:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, self.ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= self.COLS:
                break

            current = self.board[r][right]
            if current is None:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, self.ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves

    def get_piece(self, row, col):
        return self.board[row][col]

    def winner(self):
        if self.white_left <= 0:
            return self.BLACK
        elif self.black_left <= 0:
            return self.WHITE
        return None

    def __repr__(self):
        s = ""
        for row in range(self.ROWS):
            s += str(row) + " |"
            for col in range(self.COLS):
                piece = self.board[row][col]
                if piece:
                    s += str(piece) + "|"
                else:
                    s += " |"
            s += "\n"
        s += "   0 1 2 3 4 5 6 7"
        return s