from board import Board
from busqueda import Busqueda
from estado import Estado
import math
import time
import random

class Game:
    def __init__(self, mode="HvB"):  # HvB = Humano vs Bot, HvH = Humano vs Humano
        self.board = Board()
        self.current_player = 'w'
        self.game_over = False
        self.mode = mode
        self.repetition_history = {}
        self.turnos_sin_captura = 0
        self.max_turnos_sin_captura = 30  # Límite para empate

        if self.mode == "HvB":
            self.bot_player = 'b'
            self.search = Busqueda(self.board, self.bot_player, 'w')
        elif self.mode == "BvB":
            self.search_w = Busqueda(self.board, 'w', 'b')
            self.search_b = Busqueda(self.board, 'b', 'w')

    def switch_player(self):
        self.current_player = 'b' if self.current_player == 'w' else 'w'

    def _is_capture_move(self, start, end):
        dir_row = 1 if end[0] > start[0] else -1
        dir_col = 1 if end[1] > start[1] else -1
        r, c = start[0] + dir_row, start[1] + dir_col
        enemy_found = False
        while (r, c) != end:
            cell = self.board.board[r][c]
            if cell is not None:
                if cell.lower() != self.current_player:
                    if enemy_found:
                        return False
                    enemy_found = True
                else:
                    return False
            r += dir_row
            c += dir_col
        return enemy_found

    def play_turn(self):
        self.board.print_board()
        print(f"Turno del jugador: {self.current_player.upper()}")

        if self.mode == "HvH" or (self.mode == "HvB" and self.current_player == 'w'):
            continue_turn = True
            current_pos = None

            while continue_turn:
                if current_pos is not None:
                    moves_from_current = self.board.get_piece_moves(current_pos, self.current_player)
                    valid_moves = [move for move in moves_from_current if abs(move[0][0] - move[1][0]) == 2]
                else:
                    valid_moves = self.board.get_valid_moves(self.current_player)

                capture_moves = []
                for move in valid_moves:
                    start, end = move
                    piece = self.board.board[start[0]][start[1]]
                    if piece and piece.isupper():
                        if self.board.is_valid_capture_path(start, end, self.current_player) and self._is_capture_move(start, end):
                            capture_moves.append(move)
                    else:
                        if abs(start[0] - end[0]) == 2:
                            capture_moves.append(move)

                def validar_formato_coordenada(input_str):
                    partes = input_str.split(',')
                    return len(partes) == 2 and all(p.strip().isdigit() for p in partes)

                if current_pos is None:
                    while True:
                        start_input = input(f"Ingresa la coordenada de la pieza que quieres mover (ej: {valid_moves}): ").strip()
                        if validar_formato_coordenada(start_input):
                            start = tuple(map(int, start_input.split(',')))
                            if any(move[0] == start for move in valid_moves):
                                break
                        print("⚠️ Movimiento inválido o formato incorrecto. Intenta de nuevo.")
                else:
                    start = current_pos
                    print(f"📌 Jugada encadenada: Debes continuar desde {start}")

                while True:
                    posibles_destinos = [move[1] for move in valid_moves if move[0] == start]
                    end_input = input(f"Ingresa la coordenada destino (ej: {posibles_destinos}): ").strip()
                    if validar_formato_coordenada(end_input):
                        end = tuple(map(int, end_input.split(',')))
                        if (start, end) in valid_moves:
                            break
                    print("⚠️ Movimiento inválido o formato incorrecto. Intenta de nuevo.")

                movimiento = (start, end)

                if capture_moves and movimiento not in capture_moves:
                    print("⚠️ ¡Debes capturar! Movimiento no permitido.")
                    continue

                is_capture = self.board.move_piece(start, end)

                if is_capture:
                    self.turnos_sin_captura = 0
                    self.repetition_history.clear()
                else:
                    self.turnos_sin_captura += 1
                    current_state = self.board.get_state_representation()
                    self.repetition_history[current_state] = self.repetition_history.get(current_state, 0) + 1
                    if self.repetition_history[current_state] >= 3:
                        print("¡Empate por 3 repeticiones sin capturas!")
                        self.game_over = True

                if is_capture:
                    moves = self.board.get_piece_moves(end, self.current_player)
                    possible_captures = [move for move in moves if abs(move[0][0] - move[1][0]) == 2]
                    if possible_captures:
                        print("✨ ¡Captura encadenada disponible!")
                        current_pos = end
                        continue

                continue_turn = False
                self.switch_player()
        else:
            print("Bot pensando...")
            current_search = self.search_w if self.current_player == 'w' else self.search_b if self.mode == "BvB" else self.search
            estado_actual = Estado(self.board, self.current_player)
            valid_moves = estado_actual.get_valid_moves()

            capture_moves = []
            for move in valid_moves:
                start, end = move
                piece = self.board.board[start[0]][start[1]]
                if piece and piece.isupper():
                    if self.board.is_valid_capture_path(start, end, self.current_player) and self._is_capture_move(start, end):
                        capture_moves.append(move)
                else:
                    if abs(start[0] - end[0]) == 2:
                        capture_moves.append(move)

            if capture_moves:
                valid_moves = capture_moves

            best_value = -math.inf
            best_moves = []
            for move in valid_moves:
                nuevo_estado = estado_actual.move(move)
                board_value = current_search.minimax(nuevo_estado, 5, -math.inf, math.inf, False)
                if board_value > best_value:
                    best_value = board_value
                    best_moves = [move]
                elif board_value == best_value:
                    best_moves.append(move)

            best_move = random.choice(best_moves)
            print(f"Bot {self.current_player.upper()} mueve: {best_move}\n")
            is_capture = self.board.move_piece(best_move[0], best_move[1])
            self._update_game_state(is_capture)

            start, end = best_move
            if abs(start[0] - end[0]) >= 2:
                moves = self.board.get_piece_moves(end, self.current_player)
                possible_captures = []
                for move in moves:
                    s, e = move
                    p = self.board.board[s[0]][s[1]]
                    if p and p.isupper():
                        if self.board.is_valid_capture_path(s, e, self.current_player) and self._is_capture_move(s, e):
                            possible_captures.append(move)
                    else:
                        if abs(s[0] - e[0]) == 2:
                            possible_captures.append(move)

                if possible_captures:
                    print("✨ ¡El bot tiene captura encadenada! Sigue moviendo...")
                    current_pos = end
                    while possible_captures:
                        best_move = possible_captures[0]
                        print(f"El bot mueve {best_move}")
                        self.board.move_piece(best_move[0], best_move[1])
                        start, end = best_move
                        moves = self.board.get_piece_moves(end, self.current_player)
                        possible_captures = []
                        for move in moves:
                            s, e = move
                            p = self.board.board[s[0]][s[1]]
                            if p and p.isupper():
                                if self.board.is_valid_capture_path(s, e, self.current_player) and self._is_capture_move(s, e):
                                    possible_captures.append(move)
                            else:
                                if abs(s[0] - e[0]) == 2:
                                    possible_captures.append(move)
                        current_pos = end

            self.switch_player()

    def _update_game_state(self, is_capture):
        if is_capture:
            self.turnos_sin_captura = 0
            self.repetition_history.clear()
        else:
            self.turnos_sin_captura += 1
            current_state = self.board.get_state_representation()
            self.repetition_history[current_state] = self.repetition_history.get(current_state, 0) + 1

            if self.repetition_history[current_state] >= 3:
                print("¡Empate por 3 repeticiones sin capturas!")
                self.board.print_board()
                self.game_over = True

        if self.turnos_sin_captura >= self.max_turnos_sin_captura:
            print("¡Empate por límite de turnos sin capturas!")
            self.board.print_board()
            self.game_over = True

    def _get_opponent(self, player):
        return 'b' if player == 'w' else 'w'

    def play_game(self):
        while not self.game_over:
            self.play_turn()
            if self.game_over:
                break

            if self.mode == "BvB":
                time.sleep(0)

            current_player = self.current_player
            opponent = self._get_opponent(current_player)

            if self.board.count_pieces(current_player) == 0:
                print(f"🎉 ¡Jugador {opponent.upper()} gana! {current_player.upper()} no tiene piezas.")
                self.board.print_board()
                self.game_over = True
            elif not self.board.has_valid_moves(current_player):
                print(f"🎉 ¡Jugador {opponent.upper()} gana! {current_player.upper()} no tiene movimientos.")
                self.board.print_board()
                self.game_over = True
            elif not self.board.has_valid_moves('w') and not self.board.has_valid_moves('b'):
                print("🏁 ¡Empate! Ambos jugadores sin movimientos válidos.")
                self.board.print_board()
                self.game_over = True
    