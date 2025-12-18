class Board:
    def __init__(self):
        self.board = self.create_board()
        self.history = []

    def create_board(self):
        board = []
        for row in range(8):
            board_row = [None] * 8
            board.append(board_row)
        for row in range(8):
            if row % 2 == 0:
                for col in range(1, 8, 2):
                    if row < 3:
                        board[row][col] = 'b'
                    elif row > 4:
                        board[row][col] = 'w'
            else:
                for col in range(0, 8, 2):
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
        is_capture = False  # Flag para captura

        self.history.append((start_row, start_col, end_row, end_col, self.board[start_row][start_col], self.board[end_row][end_col]))

        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = None

        if abs(start_row - end_row) > 1:
            dir_row = 1 if end_row > start_row else -1
            dir_col = 1 if end_col > start_col else -1
            r, c = start_row + dir_row, start_col + dir_col
            while r != end_row and c != end_col:
                if self.board[r][c] is not None:
                    self.board[r][c] = None
                    is_capture = True  # ¡Captura detectada!
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

        # Movimiento debe ser en diagonal
        row_diff = end_row - start_row
        col_diff = end_col - start_col

        if abs(row_diff) != abs(col_diff):
            return False

        # PIEZA NORMAL
        if piece.islower():
            if player == 'w' and row_diff > 0:
                return False
            if player == 'b' and row_diff < 0:
                return False
            if abs(row_diff) > 2:  # piezas normales no saltan más de 2
                return False

        # PIEZA DAMA
        if piece.isupper():
            return self.is_valid_capture_path(start, end, player)

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
                    return False  # bloqueado por propia pieza
                else:
                    enemy_pieces += 1
                    if enemy_pieces > 1:
                        return False  # más de una pieza enemiga
            r += dir_row
            c += dir_col

        # Si movimiento fue de exactamente 2 casillas, solo puede capturar si hay una pieza enemiga
        if abs(start_row - end_row) == 2:
            return enemy_pieces == 1

        # Para movimientos largos de Dama
        if enemy_pieces == 0:
            return True  # movimiento libre sin capturas
        elif enemy_pieces == 1:
            return True  # captura válida
        else:
            return False


    def game_over(self):
        for row in self.board:
            for cell in row:
                if cell is not None:
                    return False
        return True

    def get_valid_moves(self, player):
        valid_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.lower() == player:
                    moves = self.get_piece_moves((row, col), piece)
                    valid_moves.extend(moves)
        return valid_moves
    
    def get_valid_moves2(self, position, player):
        valid_moves = []
        start_row, start_col = position
        piece = self.board[start_row][start_col]

        if piece is None or (player == 'w' and piece.lower() != 'w') or (player == 'b' and piece.lower() != 'b'):
            return valid_moves

        # Direcciones posibles según el jugador (blancas suben, negras bajan)
        directions = []
        if player == 'w':
            directions = [(-1, -1), (-1, 1)]  # Diagonal arriba
        else:
            directions = [(1, -1), (1, 1)]    # Diagonal abajo

        # Si es una dama (mayúscula), puede moverse en todas las direcciones diagonales
        if piece.isupper():
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            end_row, end_col = start_row + dr, start_col + dc
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                if self.is_valid_move(position, (end_row, end_col), player):
                    valid_moves.append((end_row, end_col))

        return valid_moves

    def get_piece_moves(self, pos, piece):
        row, col = pos
        moves = []

        # Direcciones básicas
        dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)] if piece.isupper() else \
            [(-1, -1), (-1, 1)] if piece == 'w' else [(1, -1), (1, 1)]

        for drow, dcol in dirs:
            r1, c1 = row + drow, col + dcol          # casilla inmediata
            r2, c2 = row + 2*drow, col + 2*dcol      # casilla de salto

            # --- PIEZAS “NORMALES” -------------------------------------------------
            if piece.islower():
                # 1 paso simple
                if 0 <= r1 < 8 and 0 <= c1 < 8 and \
                self.is_valid_move((row, col), (r1, c1), piece):
                    moves.append(((row, col), (r1, c1)))

                # salto de captura
                if 0 <= r2 < 8 and 0 <= c2 < 8 and \
                self.is_valid_move((row, col), (r2, c2), piece):
                    moves.append(((row, col), (r2, c2)))
                continue  # no hay más que buscar en esa dirección

            # --- DAMAS ------------------------------------------------------------
            r, c = r1, c1
            while 0 <= r < 8 and 0 <= c < 8:
                if self.is_valid_move((row, col), (r, c), piece.lower()):
                    moves.append(((row, col), (r, c)))
                if self.board[r][c] is not None:      # pieza en el camino → parar
                    break
                r += drow
                c += dcol

        return moves
    def count_pieces(self, player):
        """Cuenta las piezas restantes de un jugador (incluyendo damas)."""
        count = 0
        for row in self.board:
            for cell in row:
                if cell is not None and cell.lower() == player:
                    count += 1
        return count

    def has_valid_moves(self, player):
        """Verifica si un jugador tiene movimientos válidos disponibles."""
        return len(self.get_valid_moves(player)) > 0
    
    def get_state_representation(self):
        """Retorna una representación única del tablero (tupla de tuplas)."""
        state = []
        for row in self.board:
            row_repr = []
            for cell in row:
                row_repr.append(cell if cell is not None else " ")
            state.append(tuple(row_repr))
        return tuple(state)