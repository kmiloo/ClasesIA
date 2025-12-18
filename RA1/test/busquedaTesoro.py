import random
import time
from collections import deque
import pygame

# Constantes
EMPTY = "_"
OBSTACLE = "X"
EXCAVATED = "E"
VISITED = "."
TREASURE = "T"
TILE_SIZE = 40
MAX_OBSTACLES = 10

# Colores
COLORS = {
    EMPTY: (255, 255, 255),
    OBSTACLE: (0, 0, 0),
    EXCAVATED: (139, 69, 19),
    VISITED: (173, 216, 230),
    TREASURE: (255, 223, 0),
    "S": (0, 255, 0),
    "EXPLORER": (255, 0, 0)
}

class Island:
    def __init__(self, width=10, height=10, num_obstacles=MAX_OBSTACLES):
        self.width = width
        self.height = height
        self.grid = [[EMPTY for _ in range(width)] for _ in range(height)]
        self.visited = set()
        self.excavations = set()
        self.start_pos = (0, 0)
        self.treasure_pos = (width-1, height-1)
        self.place_obstacles(num_obstacles)

    def place_obstacles(self, num_obstacles):
        placed = 0
        attempts = 0
        while placed < num_obstacles and attempts < 1000:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (x,y) in [self.start_pos, self.treasure_pos]:
                attempts += 1
                continue
            if self.grid[y][x] != EMPTY:
                attempts += 1
                continue
            neighbors = [(x+dx, y+dy) for dx,dy in [(-1,0),(1,0),(0,-1),(0,1)]]
            if any(0 <= nx < self.width and 0 <= ny < self.height and self.grid[ny][nx] == OBSTACLE for nx, ny in neighbors):
                attempts += 1
                continue
            self.grid[y][x] = OBSTACLE
            placed += 1

    def valid_move(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        if self.grid[y][x] == OBSTACLE:
            return False
        if (x,y) in self.excavations:
            return False
        if (x,y) in self.visited:
            return False
        return True

    def update_treasure(self):
        if self.treasure_pos is not None:
            self.excavations.add(self.treasure_pos)
            self.grid[self.treasure_pos[1]][self.treasure_pos[0]] = EXCAVATED

        possible_positions = [
            (x,y) for y in range(self.height) for x in range(self.width)
            if self.grid[y][x] == EMPTY
            and (x,y) not in self.excavations
            and (x,y) not in self.visited
            and (x,y) != self.start_pos
        ]

        if not possible_positions:
            self.treasure_pos = None
            return

        self.treasure_pos = random.choice(possible_positions)

def draw_island(screen, island, explorer_pos):
    for y in range(island.height):
        for x in range(island.width):
            tile = island.grid[y][x]
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if (x,y) == explorer_pos:
                color = COLORS["EXPLORER"]
            elif (x,y) == island.treasure_pos:
                color = COLORS[TREASURE]
            elif (x,y) in island.excavations:
                color = COLORS[EXCAVATED]
            elif (x,y) in island.visited:
                color = COLORS[VISITED]
            elif tile == OBSTACLE:
                color = COLORS[OBSTACLE]
            else:
                color = COLORS[EMPTY]

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0,0,0), rect, 1)

def draw_glossary(screen, x, y):
    font = pygame.font.SysFont(None, 24)
    items = [
        ("Explorador", COLORS["EXPLORER"]),
        ("Tesoro", COLORS[TREASURE]),
        ("Obstáculo", COLORS[OBSTACLE]),
        ("Excavación (tesoro previo)", COLORS[EXCAVATED]),
        ("Casilla visitada", COLORS[VISITED]),
        ("Vacío", COLORS[EMPTY]),
    ]
    for i, (text, color) in enumerate(items):
        rect = pygame.Rect(x, y + i*30, 25, 25)
        pygame.draw.rect(screen, color, rect)
        label = font.render(text, True, (0,0,0))
        screen.blit(label, (x + 35, y + i*30 + 2))

def get_valid_moves(island, pos):
    x, y = pos
    moves = []
    directions = [(0,1), (1,0), (0,-1), (-1,0)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if island.valid_move(nx, ny):
            moves.append((nx, ny))
    return moves

def bfs_path(island, start, goal):
    if goal is None:
        return []   
    queue = deque([start])
    parents = {start: None}
    while queue:
        current = queue.popleft()
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = parents[current]
            path.reverse()
            return path[1:]
        for neighbor in get_valid_moves(island, current):
            if neighbor not in parents:
                parents[neighbor] = current
                queue.append(neighbor)
    return []

def initialize_game(width, height):
    island = Island(width, height)
    explorer_pos = island.start_pos
    island.visited.add(explorer_pos)
    path = bfs_path(island, explorer_pos, island.treasure_pos)
    return island, explorer_pos, path

def draw_restart_button(screen, font):
    button_rect = pygame.Rect(630, 350, 150, 50)
    pygame.draw.rect(screen, (200, 200, 100), button_rect)
    text = font.render("Reiniciar", True, (0, 0, 0))
    screen.blit(text, (button_rect.x + 25, button_rect.y + 10))
    return button_rect

def main():
    pygame.init()
    width, height = 10, 10
    screen_width = width * TILE_SIZE + 370
    screen_height = height * TILE_SIZE

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Búsqueda del Tesoro")
    font = pygame.font.SysFont(None, 32)
    small_font = pygame.font.SysFont(None, 24)

    modo = None
    clock = pygame.time.Clock()
    message = ""
    game_over = False
    restart_button = None
    move_count = 0  

    # Menú de selección de modo
    selecting = True
    while selecting:
        screen.fill((220,220,220))
        title = font.render("Seleccione modo:", True, (0,0,0))
        screen.blit(title, (300, 200))

        auto_button = pygame.Rect(50, 120, 200, 50)
        paso_button = pygame.Rect(50, 200, 200, 50)

        pygame.draw.rect(screen, (100,200,100), auto_button)
        pygame.draw.rect(screen, (100,100,200), paso_button)

        auto_text = font.render("Automático", True, (0,0,0))
        paso_text = font.render("Paso a paso", True, (0,0,0))

        screen.blit(auto_text, (auto_button.x + 25, auto_button.y + 10))
        screen.blit(paso_text, (paso_button.x + 25, paso_button.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if auto_button.collidepoint(mx, my):
                    modo = "auto"
                    selecting = False
                elif paso_button.collidepoint(mx, my):
                    modo = "paso"
                    selecting = False

        pygame.display.flip()
        clock.tick(30)

    # Inicializar juego
    island, explorer_pos, path = initialize_game(width, height)
    if not path:
        message = "No hay camino inicial!"
        game_over = True

    running = True
    move_ready = (modo == "auto")
    last_move_time = time.time()
    moves_since_treasure = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if restart_button.collidepoint(mx, my):
                    # Reiniciar juego
                    island, explorer_pos, path = initialize_game(width, height)
                    game_over = False
                    message = ""
                    moves_since_treasure = 0
                    move_count = 0  
                    if not path:
                        message = "No hay camino inicial!"
                        game_over = True
            if not game_over and modo == "paso" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    move_ready = True

        if not game_over:
            if modo == "auto" and time.time() - last_move_time > 1.5:
                move_ready = True
                last_move_time = time.time()

            if move_ready and path:
                next_pos = path.pop(0)
                if next_pos in get_valid_moves(island, explorer_pos):
                    explorer_pos = next_pos
                    island.visited.add(explorer_pos)
                    moves_since_treasure += 1
                    move_count += 1  
                    if explorer_pos == island.treasure_pos:
                        island.excavations.add(island.treasure_pos)
                        island.grid[island.treasure_pos[1]][island.treasure_pos[0]] = EXCAVATED
                        message = "¡Tesoro encontrado! Fin del juego."
                        game_over = True
                    else:
                        if moves_since_treasure >= 3:
                            moves_since_treasure = 0
                            island.update_treasure()
                            if island.treasure_pos is None:
                                message = "¡No hay más movimientos!"
                                game_over = True
                            else:
                                path = bfs_path(island, explorer_pos, island.treasure_pos)
                                if not path:
                                    message = "¡Camino bloqueado!"
                                    game_over = True

                    move_ready = False if modo == "paso" else True
                else:
                    path = bfs_path(island, explorer_pos, island.treasure_pos)
                    if not path:
                        message = "¡Camino bloqueado!"
                        game_over = True
                    move_ready = False if modo == "paso" else True

        # Dibujado
        screen.fill((220,220,220))
        draw_island(screen, island, explorer_pos)
        draw_glossary(screen, width * TILE_SIZE + 20, 20)

        # Mensajes y contador
        if message:
            msg_text = small_font.render(message, True, (255, 0, 0))
            screen.blit(msg_text, (width * TILE_SIZE + 20, 250))
        
        # Mostrar contador de movimientos
        count_text = small_font.render(f"Movimientos: {move_count}", True, (0, 0, 0))
        screen.blit(count_text, (width * TILE_SIZE + 20, 300))

        # Botón de reinicio
        if game_over:
            restart_button = draw_restart_button(screen, font)

        # Información de modo
        modo_text = font.render(f"Modo: {'Automático' if modo == 'auto' else 'Paso a paso'}", True, (0,0,0))
        screen.blit(modo_text, (width * TILE_SIZE + 20, height * TILE_SIZE - 50))

        if modo == "paso" and not game_over:
            info_text = font.render("Presiona ESPACIO para avanzar", True, (0,0,0))
            screen.blit(info_text, (width * TILE_SIZE + 20, height * TILE_SIZE - 80))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()