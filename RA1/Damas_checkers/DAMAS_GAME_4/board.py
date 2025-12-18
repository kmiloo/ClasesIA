class Board:
    def __init__(self):
        self.board = self.create_board()
        self.history = []

    def create_board(self):
        board = [[None] * 8 for _ in range(8)]
        for row in range(8):
            cols = range(1, 8, 2) if row % 2 == 0 else range(0, 8, 2)
            for col in cols:
                if row < 3:
                    board[row][col] = 'b'
                elif row > 4:
                    board[row][col] = 'w'
        return board

    def print_board(self):
        print("    0 1 2 3 4 5 6 7")
        print("                  ")
        for row_index, row in enumerate(self.board):
            print(f"{row_index}  ", " ".join(['-' if x is None else x for x in row]))
        print()

    def move_piece(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        piece = self.board[start_row][start_col]
        is_capture = False

        self.history.append((start_row, start_col, end_row, end_col,
                              self.board[start_row][start_col],
                              self.board[end_row][end_col]))

        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = None

        if abs(start_row - end_row) > 1:
            dir_row = 1 if end_row > start_row else -1
            dir_col = 1 if end_col > start_col else -1
            r, c = start_row + dir_row, start_col + dir_col
            while r != end_row and c != end_col:
                if self.board[r][c] is not None:
                    self.board[r][c] = None
                    is_capture = True
                    break
                r += dir_row
                c += dir_col

        if piece == 'w' and end_row == 0:
            self.board[end_row][end_col] = 'W'
        elif piece == 'b' and end_row == 7:
            self.board[end_row][end_col] = 'B'

        return is_capture

    def undo_move(self):
        if self.history:
            start_row, start_col, end_row, end_col, piece, captured = self.history.pop()
            self.board[start_row][start_col] = piece
            self.board[end_row][end_col] = captured

    def is_valid_move(self, start, end, player):
        start_row, start_col = start
        end_row, end_col = end

        if not (0 <= end_row < 8 and 0 <= end_col < 8):
            return False

        piece = self.board[start_row][start_col]
        if piece is None:
            return False

        if (player == 'w' and piece.lower() != 'w') or (player == 'b' and piece.lower() != 'b'):
            return False
 
        if self.board[end_row][end_col] is not None:
            return False

        row_diff = end_row - start_row
        col_diff = end_col - start_col
        if abs(row_diff) != abs(col_diff):
            return False

        if piece.islower():
            # Dirección correcta
            if player == 'w' and row_diff > 0:
                return False
            if player == 'b' and row_diff < 0:
                return False
            # Solo un paso o captura de dos
            if abs(row_diff) > 2:
                return False

        return self.is_valid_capture_path(start, end, player)

    def is_valid_capture_path(self, start, end, player):
        start_row, start_col = start
        end_row, end_col = end

        if abs(start_row - end_row) != abs(start_col - end_col):
            return False

        dir_row = 1 if end_row > start_row else -1
        dir_col = 1 if end_col > start_col else -1

        r, c = start_row + dir_row, start_col + dir_col
        enemy_pieces = 0
        while r != end_row and c != end_col:
            if self.board[r][c] is not None:
                if self.board[r][c].lower() == player:
                    return False 
                else:
                    enemy_pieces += 1
                    if enemy_pieces > 1:
                        return False 
            r += dir_row
            c += dir_col

        if abs(start_row - end_row) == 2:
            return enemy_pieces == 1

        return enemy_pieces <= 1

    def get_piece_moves(self, pos, piece):
        row, col = pos
        moves = []

        dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)] if piece.isupper() else \
               [(-1, -1), (-1, 1)] if piece == 'w' else [(1, -1), (1, 1)]

        for drow, dcol in dirs:
            r1, c1 = row + drow, col + dcol    
            r2, c2 = row + 2 * drow, col + 2 * dcol

            if piece.islower():
                if 0 <= r1 < 8 and 0 <= c1 < 8 and self.is_valid_move((row, col), (r1, c1), piece):
                    moves.append(((row, col), (r1, c1)))
                if 0 <= r2 < 8 and 0 <= c2 < 8 and self.is_valid_move((row, col), (r2, c2), piece):
                    moves.append(((row, col), (r2, c2)))
                continue

            r, c = r1, c1
            enemy_found = False
            while 0 <= r < 8 and 0 <= c < 8:
                square = self.board[r][c]
                if square is None:
                    if self.is_valid_move((row, col), (r, c), piece.lower()):
                        moves.append(((row, col), (r, c)))
                else:
                    if square.lower() == piece.lower() or enemy_found:
                        break 
                    enemy_found = True 
                r += drow
                c += dcol

        return moves

    def game_over(self):
        return all(cell is None for row in self.board for cell in row)

    def get_valid_moves(self, player):
        valid = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.lower() == player:
                    valid.extend(self.get_piece_moves((row, col), piece))
        return valid

    def get_valid_moves2(self, position, player):
        valid = []
        start_row, start_col = position
        piece = self.board[start_row][start_col]
        if piece is None or piece.lower() != player:
            return valid

        dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)] if piece.isupper() else \
               [(-1, -1), (-1, 1)] if player == 'w' else [(1, -1), (1, 1)]
        for drow, dcol in dirs:
            end_row, end_col = start_row + drow, start_col + dcol
            if 0 <= end_row < 8 and 0 <= end_col < 8 and self.is_valid_move(position, (end_row, end_col), player):
                valid.append((end_row, end_col))
        return valid

    def count_pieces(self, player):
        return sum(1 for row in self.board for cell in row if cell and cell.lower() == player)

    def has_valid_moves(self, player):
        return bool(self.get_valid_moves(player))

    def get_state_representation(self):
        return tuple(tuple(cell if cell is not None else " " for cell in row) for row in self.board)
