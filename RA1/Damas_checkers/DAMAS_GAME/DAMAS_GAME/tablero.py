class Tablero:
    def __init__(self):
        self.tablero = self.crear_tablero()
        self.historial = []

    def crear_tablero(self):
        tablero = []
        for fila in range(8):
            fila_tablero = [None] * 8
            tablero.append(fila_tablero)
        for fila in range(8):
            if fila % 2 == 0:
                for col in range(1, 8, 2):
                    if fila < 3:
                        tablero[fila][col] = 'b'
                    elif fila > 4:
                        tablero[fila][col] = 'w'
            else:
                for col in range(0, 8, 2):
                    if fila < 3:
                        tablero[fila][col] = 'b'
                    elif fila > 4:
                        tablero[fila][col] = 'w'
        return tablero

    def imprimir_tablero(self):
        print("    0 1 2 3 4 5 6 7")
        print("                  ")
        for index_fila, fila in enumerate(self.tablero):
            print(f"{index_fila}  ", " ".join(['-' if x is None else x for x in fila]))
        print()

    def mover_pieza(self, inicio, fin):
        fila_inicio, col_inicio = inicio
        fila_fin, col_fin = fin
        pieza = self.tablero[fila_inicio][col_inicio]
        es_captura = False

        self.historial.append((fila_inicio, col_inicio, fila_fin, col_fin, self.tablero[fila_inicio][col_inicio], self.tablero[fila_fin][col_fin]))

        self.tablero[fila_fin][col_fin] = pieza
        self.tablero[fila_inicio][col_inicio] = None

        if abs(fila_inicio - fila_fin) > 1:
            dir_fila = 1 if fila_fin > fila_inicio else -1
            dir_col = 1 if col_fin > col_inicio else -1
            f, c = fila_inicio + dir_fila, col_inicio + dir_col
            while f != fila_fin and c != col_fin:
                if self.tablero[f][c] is not None:
                    self.tablero[f][c] = None
                    es_captura = True
                    break
                f += dir_fila
                c += dir_col

        if pieza == 'w' and fila_fin == 0:
            self.tablero[fila_fin][col_fin] = 'W'
        elif pieza == 'b' and fila_fin == 7:
            self.tablero[fila_fin][col_fin] = 'B'

        return es_captura


    def deshacer_movimiento(self):
        if self.historial:
            fila_inicio, col_inicio, fila_fin, col_fin, pieza, capturada = self.historial.pop()
            self.tablero[fila_inicio][col_inicio] = pieza
            self.tablero[fila_fin][col_fin] = capturada

    def es_movimiento_valido(self, inicio, fin, jugador):
        fila_inicio, col_inicio = inicio
        fila_fin, col_fin = fin

        if not (0 <= fila_fin < 8 and 0 <= col_fin < 8):
            return False

        pieza = self.tablero[fila_inicio][col_inicio]

        if pieza is None:
            return False

        if (jugador == 'w' and pieza.lower() != 'w') or (jugador == 'b' and pieza.lower() != 'b'):
            return False

        if self.tablero[fila_fin][col_fin] is not None:
            return False

        diff_fila = fila_fin - fila_inicio
        diff_col = col_fin - col_inicio

        if abs(diff_fila) != abs(diff_col):
            return False

        if pieza.islower():
            if jugador == 'w' and diff_fila > 0:
                return False
            if jugador == 'b' and diff_fila < 0:
                return False
            if abs(diff_fila) > 2:
                return False

        if pieza.isupper():
            return self.es_camino_valido_de_captura(inicio, fin, jugador)

        return self.es_camino_valido_de_captura(inicio, fin, jugador)


    def es_camino_valido_de_captura(self, inicio, fin, jugador):
        fila_inicio, col_inicio = inicio
        fila_fin, col_fin = fin

        if abs(fila_inicio - fila_fin) != abs(col_inicio - col_fin):
            return False

        dir_fila = 1 if fila_fin > fila_inicio else -1
        dir_col = 1 if col_fin > col_inicio else -1

        f, c = fila_inicio + dir_fila, col_inicio + dir_col
        piezas_enemigas = 0

        while f != fila_fin and c != col_fin:
            if self.tablero[f][c] is not None:
                if self.tablero[f][c].lower() == jugador:
                    return False 
                else:
                    piezas_enemigas += 1
                    if piezas_enemigas > 1:
                        return False 
            f += dir_fila
            c += dir_col

        if abs(fila_inicio - fila_fin) == 2:
            return piezas_enemigas == 1

        if piezas_enemigas == 0:
            return True 
        elif piezas_enemigas == 1:
            return True  
        else:
            return False


    def fin_juego(self):
        for fila in self.tablero:
            for celda in fila:
                if celda is not None:
                    return False
        return True

    def obtener_movimientos_validos(self, jugador):
        movimientos_validos = []
        for fila in range(8):
            for col in range(8):
                pieza = self.tablero[fila][col]
                if pieza and pieza.lower() == jugador:
                    movimientos = self.obtener_movimientos_de_pieza((fila, col), pieza)
                    movimientos_validos.extend(movimientos)
        return movimientos_validos
    
    def obtener_movimientos_validos2(self, posicion, jugador):
        movimientos_validos = []
        fila_inicio, col_inicio = posicion
        pieza = self.tablero[fila_inicio][col_inicio]

        if pieza is None or (jugador == 'w' and pieza.lower() != 'w') or (jugador == 'b' and pieza.lower() != 'b'):
            return movimientos_validos

        direcciones = []
        if jugador == 'w':
            direcciones = [(-1, -1), (-1, 1)]  
        else:
            direcciones = [(1, -1), (1, 1)]   

        if pieza.isupper():
            direcciones = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in direcciones:
            fila_fin, col_fin = fila_inicio + dr, col_inicio + dc
            if 0 <= fila_fin < 8 and 0 <= col_fin < 8:
                if self.es_movimiento_valido(posicion, (fila_fin, col_fin), jugador):
                    movimientos_validos.append((fila_fin, col_fin))

        return movimientos_validos

    def obtener_movimientos_de_pieza(self, pos, pieza):
        fila, col = pos
        movimientos = []

        dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)] if pieza.isupper() else \
            [(-1, -1), (-1, 1)] if pieza == 'w' else [(1, -1), (1, 1)]

        for d_fila, d_col in dirs:
            f1, c1 = fila + d_fila, col + d_col         
            f2, c2 = fila + 2*d_fila, col + 2*d_col     

            if pieza.islower():
                if 0 <= f1 < 8 and 0 <= c1 < 8 and \
                self.es_movimiento_valido((fila, col), (f1, c1), pieza):
                    movimientos.append(((fila, col), (f1, c1)))

                if 0 <= f2 < 8 and 0 <= c2 < 8 and \
                self.es_movimiento_valido((fila, col), (f2, c2), pieza):
                    movimientos.append(((fila, col), (f2, c2)))
                continue 

            f, c = f1, c1
            while 0 <= f < 8 and 0 <= c < 8:
                if self.es_movimiento_valido((fila, col), (f, c), pieza.lower()):
                    movimientos.append(((fila, col), (f, c)))
                if self.tablero[f][c] is not None:      
                    break
                f += d_fila
                c += d_col

        return movimientos
    def contar_piezas(self, jugador):
        contador = 0
        for fila in self.tablero:
            for celda in fila:
                if celda is not None and celda.lower() == jugador:
                    contador += 1
        return contador

    def tiene_movimientos_validos(self, jugador):
        return len(self.obtener_movimientos_validos(jugador)) > 0
    
    def obtener_representacion_estado(self):
        estado = []
        for fila in self.tablero:
            fila_repr = []
            for celda in fila:
                fila_repr.append(celda if celda is not None else " ")
            estado.append(tuple(fila_repr))
        return tuple(estado)
