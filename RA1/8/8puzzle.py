from collections import deque

def resolver_8_puzzle(estado_inicial):
    """Resuelve el 8-puzzle usando BFS desde un estado inicial dado"""
    estado_objetivo = "12345678H"
    
    if estado_inicial == estado_objetivo:
        return ["Ya está resuelto"]
    
    # Inicializar estructuras de datos
    cola = deque()
    visitados = set()
    padres = {}  # Almacena (estado_previo, movimiento)
    
    # Configuración inicial
    cola.append(estado_inicial)
    visitados.add(estado_inicial)
    padres[estado_inicial] = (None, None)
    
    while cola:
        estado_actual = cola.popleft()
        
        if estado_actual == estado_objetivo:
            # Reconstruir el camino
            camino = []
            movimientos = []
            while estado_actual:
                camino.append(estado_actual)
                estado_actual, movimiento = padres[estado_actual]
                if movimiento:
                    movimientos.append(movimiento)
            camino.reverse()
            movimientos.reverse()
            return camino, movimientos
        
        # Generar estados vecinos
        pos_H = estado_actual.index('H')
        fila, col = pos_H // 3, pos_H % 3  # Convertir posición a coordenadas 3x3
        
        # Movimientos posibles (arriba, abajo, izquierda, derecha)
        movimientos = [
            (-1, 0, 'Arriba'),
            (1, 0, 'Abajo'),
            (0, -1, 'Izquierda'),
            (0, 1, 'Derecha')
        ]
        
        for df, dc, movimiento in movimientos:
            nueva_fila, nueva_col = fila + df, col + dc
            
            if 0 <= nueva_fila < 3 and 0 <= nueva_col < 3:
                nueva_pos = nueva_fila * 3 + nueva_col
                nuevo_estado = list(estado_actual)
                # Intercambiar H con la pieza adyacente
                nuevo_estado[pos_H], nuevo_estado[nueva_pos] = nuevo_estado[nueva_pos], nuevo_estado[pos_H]
                nuevo_estado = ''.join(nuevo_estado)
                
                if nuevo_estado not in visitados:
                    visitados.add(nuevo_estado)
                    padres[nuevo_estado] = (estado_actual, movimiento)
                    cola.append(nuevo_estado)
    
    return ["No se encontró solución"], []

def imprimir_solucion(camino, movimientos):
    """Muestra la solución paso a paso"""
    print("\nSolución encontrada:")
    print(f"Pasos requeridos: {len(camino)-1}")
    print("\nSecuencia de movimientos:")
    
    for i in range(1, len(camino)):
        print(f"\nPaso {i}: Mover {movimientos[i-1]}")
        imprimir_tablero(camino[i])

def imprimir_tablero(estado):
    """Muestra el tablero de 3x3"""
    print("+---+---+---+")
    for i in range(0, 9, 3):
        fila = estado[i:i+3]
        print("| " + " | ".join(fila) + " |")
        print("+---+---+---+")

# Ejemplo de uso
if __name__ == "__main__":
    estado_inicial = "123H56478"
    camino, movimientos = resolver_8_puzzle(estado_inicial)
    
    if camino[0] == "No se encontró solución":
        print(camino[0])
    else:
        imprimir_solucion(camino, movimientos)