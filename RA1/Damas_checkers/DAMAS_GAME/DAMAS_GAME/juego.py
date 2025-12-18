from tablero import Tablero
from busqueda import Busqueda
from estado import Estado
import math
import time
import random

class Juego:
    def __init__(self, modo="HvB"):  
        self.tablero = Tablero()
        self.jugador_actual = 'w'
        self.juego_terminado = False
        self.modo = modo
        self.historial_repeticiones = {}
        self.turnos_sin_captura = 0
        self.max_turnos_sin_captura = 30  
        self.turnos_totales = 0
        self.tiempo_inicio = None

        if self.modo == "HvB":
            self.jugador_bot = 'b'
            self.busqueda = Busqueda(self.tablero, self.jugador_bot, 'w')
        elif self.modo == "BvB":
            self.busqueda_w = Busqueda(self.tablero, 'w', 'b') 
            self.busqueda_b = Busqueda(self.tablero, 'b', 'w') 

    def cambiar_jugador(self):
        self.jugador_actual = 'b' if self.jugador_actual == 'w' else 'w'

    def _es_movimiento_de_captura(self, inicio, fin):
        dir_fila = 1 if fin[0] > inicio[0] else -1
        dir_columna = 1 if fin[1] > inicio[1] else -1
        f, c = inicio[0] + dir_fila, inicio[1] + dir_columna
        enemigo_encontrado = False
        while (f, c) != fin:
            celda = self.tablero.tablero[f][c]
            if celda is not None:
                if celda.lower() != self.jugador_actual:
                    if enemigo_encontrado:
                        return False
                    enemigo_encontrado = True
                else:
                    return False
            f += dir_fila
            c += dir_columna
        return enemigo_encontrado

    def jugar_turno(self):
        self.tablero.imprimir_tablero()
        print(f"Turno del jugador: {self.jugador_actual.upper()}")

        if self.modo == "HvH" or (self.modo == "HvB" and self.jugador_actual == 'w'):
            continuar_turno = True
            posicion_actual = None

            while continuar_turno:
                movimientos_validos = self.tablero.obtener_movimientos_validos(self.jugador_actual)

                movimientos_de_captura = []
                for movimiento in movimientos_validos:
                    inicio, fin = movimiento
                    pieza = self.tablero.tablero[inicio[0]][inicio[1]]
                    if pieza and pieza.isupper():
                        if self.tablero.es_camino_de_captura_valido(inicio, fin, self.jugador_actual) and self._es_movimiento_de_captura(inicio, fin):
                            movimientos_de_captura.append(movimiento)
                    else:
                        if abs(inicio[0] - fin[0]) == 2:
                            movimientos_de_captura.append(movimiento)

                inicios_de_captura = set(movimiento[0] for movimiento in movimientos_de_captura)

                def validar_formato_coordenada(cadena_entrada):
                    partes = cadena_entrada.split(',')
                    return len(partes) == 2 and all(p.strip().isdigit() for p in partes)

                if posicion_actual is None:
                    while True:
                        entrada_inicio = input(f"Ingresa la coordenada de la pieza que quieres mover (ej: 5,0): ")
                        if validar_formato_coordenada(entrada_inicio):
                            inicio = tuple(map(int, entrada_inicio.split(',')))
                            break
                        print("Formato incorrecto. Debe ser fila,columna (ej: 5,0)")

                while True:
                    entrada_fin = input(f"Ingresa la coordenada destino (ej: 4,1): ")
                    if validar_formato_coordenada(entrada_fin):
                        fin = tuple(map(int, entrada_fin.split(',')))
                        break
                    print("Formato incorrecto. Debe ser fila, columna (ej: 4,1)")
                print("\n")

                movimiento = (inicio, fin)

                if not self.tablero.es_movimiento_valido(inicio, fin, self.jugador_actual):
                    print("MOVIMIENTO ILEGAL. INTENTA DE NUEVO.")
                    continue

                if movimientos_de_captura and movimiento not in movimientos_de_captura:
                    print("Debes capturar. Movimiento no permitido.")
                    continue

                es_captura = self.tablero.mover_pieza(inicio, fin)  

                if es_captura:
                    self.turnos_sin_captura = 0
                    self.historial_repeticiones.clear()
                else:
                    self.turnos_sin_captura += 1
                    estado_actual = self.tablero.obtener_representacion_estado()
                    self.historial_repeticiones[estado_actual] = self.historial_repeticiones.get(estado_actual, 0) + 1
                    if self.historial_repeticiones[estado_actual] >= 3:
                        print("¡Empate por 3 repeticiones sin capturas!")
                        self.juego_terminado = True

                if abs(inicio[0] - fin[0]) >= 2:
                    movimientos = self.tablero.obtener_movimientos_de_pieza(fin, self.jugador_actual)
                    capturas_posibles = [movimiento for movimiento in movimientos if abs(movimiento[0][0] - movimiento[1][0]) == 2]
                    if capturas_posibles:
                        posicion_actual = fin
                        continuar_turno = True
                        continue

                continuar_turno = False
                self.cambiar_jugador()
        else:
            print("Bot pensando...")
            if self.modo == "BvB":
                if self.jugador_actual == 'w':
                    busqueda_actual = self.busqueda_w
                else:
                    busqueda_actual = self.busqueda_b
            else:
                busqueda_actual = self.busqueda  


            estado_actual = Estado(self.tablero, self.jugador_actual)
            movimientos_validos = estado_actual.obtener_movimientos_validos()

            movimientos_de_captura = []
            for movimiento in movimientos_validos:
                inicio, fin = movimiento
                pieza = self.tablero.tablero[inicio[0]][inicio[1]]
                if pieza and pieza.isupper():
                    if self.tablero.es_camino_valido_de_captura(inicio, fin, self.jugador_actual) and self._es_movimiento_de_captura(inicio, fin):
                        movimientos_de_captura.append(movimiento)
                else:
                    if abs(inicio[0] - fin[0]) == 2:
                        movimientos_de_captura.append(movimiento)

            if movimientos_de_captura:
                movimientos_validos = movimientos_de_captura

            mejores_movimientos = [] 
            mejor_valor = -math.inf
            for movimiento in movimientos_validos:
                nuevo_estado = estado_actual.mover(movimiento)
                valor_tablero = busqueda_actual.minimax(nuevo_estado, 5, -math.inf, math.inf, False)
                if valor_tablero > mejor_valor:
                    mejor_valor = valor_tablero
                    mejores_movimientos = [movimiento]
                elif valor_tablero == mejor_valor:
                    mejores_movimientos.append(movimiento)

            mejor_movimiento = random.choice(mejores_movimientos) 

            print(f"Bot {self.jugador_actual.upper()} mueve: {mejor_movimiento}\n")
            es_captura = self.tablero.mover_pieza(mejor_movimiento[0], mejor_movimiento[1])
            self._actualizar_estado_juego(es_captura)

            inicio, fin = mejor_movimiento
            if abs(inicio[0] - fin[0]) >= 2:
                movimientos = self.tablero.obtener_movimientos_de_pieza(fin, self.jugador_actual)
                capturas_posibles = []
                for movimiento in movimientos:
                    s, e = movimiento
                    p = self.tablero.tablero[s[0]][s[1]]
                    if p and p.isupper():
                        if self.tablero.es_camino_valido_de_captura(s, e, self.jugador_actual) and self._es_movimiento_de_captura(s, e):
                            capturas_posibles.append(movimiento)
                    else:
                        if abs(s[0] - e[0]) == 2:
                            capturas_posibles.append(movimiento)

                if capturas_posibles:
                    print("El bot ataca de encadenada. Se sigue moviendo como un pro")
                    posicion_actual = fin
                    while capturas_posibles:
                        mejor_movimiento = capturas_posibles[0]
                        print(f"El bot mueve {mejor_movimiento}")
                        self.tablero.mover_pieza(mejor_movimiento[0], mejor_movimiento[1])
                        inicio, fin = mejor_movimiento
                        movimientos = self.tablero.obtener_movimientos_de_pieza(fin, self.jugador_actual)
                        capturas_posibles = []
                        for movimiento in movimientos:
                            s, e = movimiento
                            p = self.tablero.tablero[s[0]][s[1]]
                            if p and p.isupper():
                                if self.tablero.es_camino_valido_de_captura(s, e, self.jugador_actual) and self._es_movimiento_de_captura(s, e):
                                    capturas_posibles.append(movimiento)
                            else:
                                if abs(s[0] - e[0]) == 2:
                                    capturas_posibles.append(movimiento)
                        posicion_actual = fin

            self.cambiar_jugador()

    def _actualizar_estado_juego(self, es_captura):
        if es_captura:
            self.turnos_sin_captura = 0
            self.historial_repeticiones.clear()  
        else:
            self.turnos_sin_captura += 1

        estado_actual = self.tablero.obtener_representacion_estado()
        self.historial_repeticiones[estado_actual] = self.historial_repeticiones.get(estado_actual, 0) + 1

        if self.historial_repeticiones[estado_actual] >= 3:
            print(f"Empate por 3 repeticiones sin capturar {self.turnos_totales} turnos.{time.time()-self.tiempo_inicio} segundos.")
            self.tablero.imprimir_tablero()
            self.juego_terminado = True

        if self.turnos_sin_captura >= self.max_turnos_sin_captura:
            print(f"Empate por limite de turnos sin capturar piezas {self.turnos_totales} turnos.{time.time()-self.tiempo_inicio} segundos.")
            self.tablero.imprimir_tablero()
            self.juego_terminado = True


    def _obtener_oponente(self, jugador):
        return 'b' if jugador == 'w' else 'w'

    def jugar_partida(self):
        self.tiempo_inicio = time.time()
        while not self.juego_terminado:
            self.turnos_totales += 1
            self.jugar_turno()
            if self.juego_terminado:
                break

            if self.modo == "BvB":
                time.sleep(0)  
            
            jugador_actual = self.jugador_actual
            oponente = self._obtener_oponente(jugador_actual)
            
            if self.tablero.contar_piezas(jugador_actual) == 0:
                print(f"Jugador {oponente.upper()} gana {jugador_actual.upper()} no tiene piezas. {self.turnos_totales} turnos.{self.tiempo_inicio-time.time()} segundos.")
                #print(f"Jugador {oponente.upper()} dice: Sencillo bro, cuando jugaras de verdad?")
                self.tablero.imprimir_tablero()
                self.juego_terminado = True
            
            elif not self.tablero.tiene_movimientos_validos(jugador_actual):
                print(f"Jugador {oponente.upper()} gana {jugador_actual.upper()} no tiene movimientos. {self.turnos_totales} turnos.{self.tiempo_inicio-time.time()} segundos.")
                #print(f"Jugador {oponente.upper()} dice: Sencillo bro, cuando jugaras de verdad?")
                self.tablero.imprimir_tablero()
                self.juego_terminado = True
            
            elif not self.tablero.tiene_movimientos_validos('w') and not self.tablero.tiene_movimientos_validos('b'):
                print(f"Empate. Ambos jugadores sin movimientos válidos. {self.turnos_totales} turnos.{self.tiempo_inicio-time.time()} segundos.")
                self.tablero.imprimir_tablero()
                self.juego_terminado = True
