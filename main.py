import pygame
from grid import make_grid, draw
from algorithms import bfs, dfs, dijkstra
import sys

pygame.init()

# Window Constants
WIDTH = 960
HEIGHT = 720
TOP_BAR_HEIGHT = 90
LEFT_PANEL_WIDTH = 250
GRID_SIZE = 600
ROWS = 30
DELAY_MS = 20

# Calculate Grid Offsets (centered in the remaining area)
X_OFFSET = LEFT_PANEL_WIDTH + (WIDTH - LEFT_PANEL_WIDTH - GRID_SIZE) // 2
Y_OFFSET = TOP_BAR_HEIGHT + (HEIGHT - TOP_BAR_HEIGHT - GRID_SIZE) // 2

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Visualizer Pro")

# Custom Themes (Modern Light Theme)
BG_COLOR = (244, 245, 247)      # Softer Background
PANEL_BG = (255, 255, 255)      # Pure white panels
BORDER_COLOR = (223, 225, 229)  # Crisp, light border
TEXT_COLOR = (32, 33, 36)       # Sharp dark gray text
TEXT_MUTED = (95, 99, 104)      # Subdued text
HIGHLIGHT = (26, 115, 232)      # Professional blue accent

# Legend Colors (Must match what grid.py sees ideally, but grid imports its own colors)
RED = (234, 67, 53)     # Google Red
GREEN = (52, 168, 83)   # Google Green
BLUE = (66, 133, 244)   # Theme Blue
YELLOW = (251, 188, 5)  # Google Yellow
BLACK = (60, 64, 67)    # Soft Black

# Safe Fonts (Using Arial for widespread compatibility and sharpness)
FONT_TITLE = pygame.font.SysFont("Arial", 22, bold=True)
FONT_BOLD = pygame.font.SysFont("Arial", 14, bold=True)
FONT_TEXT = pygame.font.SysFont("Arial", 14)

def draw_top_bar(algorithm):
    # Draw Background
    pygame.draw.rect(WIN, PANEL_BG, (0, 0, WIDTH, TOP_BAR_HEIGHT))
    pygame.draw.line(WIN, BORDER_COLOR, (0, TOP_BAR_HEIGHT - 1), (WIDTH, TOP_BAR_HEIGHT - 1), 2)
    
    # Left Side: Algorithm Title as a Badge
    alg_names = {1: "BFS", 2: "DFS", 3: "Dijkstra"}
    title_text = f"Algorithm: {alg_names[algorithm]}"
    title_surf = FONT_TITLE.render(title_text, True, (255, 255, 255))
    
    # Pill Background
    badge_padding_x = 20
    badge_padding_y = 10
    badge_w = title_surf.get_width() + badge_padding_x * 2
    badge_h = title_surf.get_height() + badge_padding_y * 2
    badge_x = int(25)
    badge_y = int(TOP_BAR_HEIGHT // 2 - badge_h // 2)
    
    pygame.draw.rect(WIN, HIGHLIGHT, (badge_x, badge_y, badge_w, badge_h), border_radius=badge_h//2)
    WIN.blit(title_surf, (int(badge_x + badge_padding_x), int(badge_y + badge_padding_y)))
    
    # Right Side: Controls (Structured in 2 Lines)
    controls_line1 = "1: BFS  |  2: DFS  |  3: Dijkstra"
    controls_line2 = "SPACE: Start  |  C: Clear"
    
    ctrl1_surf = FONT_BOLD.render(controls_line1, True, TEXT_COLOR)
    ctrl2_surf = FONT_BOLD.render(controls_line2, True, TEXT_MUTED)
    
    x_pos1 = int(WIDTH - ctrl1_surf.get_width() - 30)
    x_pos2 = int(WIDTH - ctrl2_surf.get_width() - 30)
    
    WIN.blit(ctrl1_surf, (x_pos1, int(22)))
    WIN.blit(ctrl2_surf, (x_pos2, int(48)))

def draw_side_panel():
    # Draw Background
    pygame.draw.rect(WIN, PANEL_BG, (0, TOP_BAR_HEIGHT, LEFT_PANEL_WIDTH, HEIGHT - TOP_BAR_HEIGHT))
    pygame.draw.line(WIN, BORDER_COLOR, (LEFT_PANEL_WIDTH - 1, TOP_BAR_HEIGHT), (LEFT_PANEL_WIDTH - 1, HEIGHT), 2)
    
    y_pos = int(TOP_BAR_HEIGHT + 25)
    x_pos = 20
    content_w = LEFT_PANEL_WIDTH - 40
    
    # Card 1: Instructions
    inst_h = 290
    pygame.draw.rect(WIN, BG_COLOR, (x_pos, y_pos, content_w, inst_h), border_radius=8)
    pygame.draw.rect(WIN, BORDER_COLOR, (x_pos, y_pos, content_w, inst_h), 1, border_radius=8)
    
    y_inst = y_pos + 15
    x_inst = x_pos + 15
    
    inst_head = FONT_BOLD.render("INSTRUCTIONS", True, HIGHLIGHT)
    WIN.blit(inst_head, (int(x_inst), int(y_inst)))
    y_inst += 25
    
    instructions = [
        "Press 1: Select BFS",
        "Press 2: Select DFS",
        "Press 3: Select Dijkstra",
        "",
        "First L-Click: Start Node",
        "Next L-Click: End Node",
        "Other L-Clicks: Barriers",
        "Right Click: Erase Cell",
        "SPACE: Start Search",
        "C: Clear Grid"
    ]
    
    for line in instructions:
        surf = FONT_TEXT.render(line, True, TEXT_COLOR)
        WIN.blit(surf, (int(x_inst), int(y_inst)))
        y_inst += 22
        
    y_pos += inst_h + 20
    
    # Card 2: Color Legend
    leg_h = 200
    pygame.draw.rect(WIN, BG_COLOR, (x_pos, y_pos, content_w, leg_h), border_radius=8)
    pygame.draw.rect(WIN, BORDER_COLOR, (x_pos, y_pos, content_w, leg_h), 1, border_radius=8)
    
    y_leg = y_pos + 15
    x_leg = x_pos + 15
    
    leg_head = FONT_BOLD.render("COLOR LEGEND", True, HIGHLIGHT)
    WIN.blit(leg_head, (int(x_leg), int(y_leg)))
    y_leg += 30
    
    legend_items = [
        ("Start Node", GREEN),
        ("End Node", RED),
        ("Barrier", BLACK),
        ("Visited Path", BLUE),
        ("Final Path", YELLOW)
    ]
    
    BOX_SIZE = 14
    for label, color in legend_items:
        pygame.draw.rect(WIN, color, (int(x_leg), int(y_leg), BOX_SIZE, BOX_SIZE), border_radius=3)
        lbl_surf = FONT_TEXT.render(label, True, TEXT_COLOR)
        WIN.blit(lbl_surf, (int(x_leg + BOX_SIZE + 12), int(y_leg - 1)))
        y_leg += 26

def get_clicked_pos(pos, rows, width, x_offset, y_offset):
    x, y = pos
    x -= x_offset
    y -= y_offset
    
    if x < 0 or y < 0 or x >= width or y >= width:
        return None
        
    gap = width // rows
    row = y // gap
    col = x // gap
    
    if 0 <= row < rows and 0 <= col < rows:
        return row, col
    return None

def draw_grid_container():
    # Draw modern backing behind the grid so it stands out cleanly
    pygame.draw.rect(WIN, PANEL_BG, (X_OFFSET - 2, Y_OFFSET - 2, GRID_SIZE + 4, GRID_SIZE + 4), border_radius=6)
    pygame.draw.rect(WIN, BORDER_COLOR, (X_OFFSET - 2, Y_OFFSET - 2, GRID_SIZE + 4, GRID_SIZE + 4), 1, border_radius=6)

def handle_input(event, start, end, grid, algorithm_selected, win_surface):
    run_algo = False
    if pygame.mouse.get_pressed()[0]: # Left click
        pos = pygame.mouse.get_pos()
        clicked = get_clicked_pos(pos, ROWS, GRID_SIZE, X_OFFSET, Y_OFFSET)
        if clicked:
            row, col = clicked
            node = grid[row][col]
            
            if not start and node != end:
                start = node
                start.make_start()
            elif not end and node != start:
                end = node
                end.make_end()
            elif node != start and node != end:
                node.make_wall()
                
    elif pygame.mouse.get_pressed()[2]: # Right click
        pos = pygame.mouse.get_pos()
        clicked = get_clicked_pos(pos, ROWS, GRID_SIZE, X_OFFSET, Y_OFFSET)
        if clicked:
            row, col = clicked
            node = grid[row][col]
            node.reset()
            if node == start:
                start = None
            if node == end:
                end = None
                
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_1:
            algorithm_selected = 1
        if event.key == pygame.K_2:
            algorithm_selected = 2
        if event.key == pygame.K_3:
            algorithm_selected = 3
            
        if event.key == pygame.K_SPACE and start and end:
            run_algo = True
                
        if event.key == pygame.K_c:
            start = None
            end = None
            grid = make_grid(ROWS, GRID_SIZE)

    return algorithm_selected, start, end, grid, run_algo

def main():
    grid = make_grid(ROWS, GRID_SIZE)
    
    start = None
    end = None
    
    run = True
    algorithm_selected = 1 # 1 = BFS, 2 = DFS, 3 = Dijkstra
    
    while run:
        WIN.fill(BG_COLOR)
        draw_top_bar(algorithm_selected)
        draw_side_panel()
        draw_grid_container()
        draw(WIN, grid, ROWS, GRID_SIZE, X_OFFSET, Y_OFFSET)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            algorithm_selected, start, end, grid, run_algo = handle_input(
                event, start, end, grid, algorithm_selected, WIN
            )
            
            if run_algo:
                for row in grid:
                    for node in row:
                        if node.is_visited() or node.color == YELLOW:
                            node.reset()
                            
                for row in grid:
                    for node in row:
                        node.update_neighbors(grid)
                
                def draw_func():
                    WIN.fill(BG_COLOR)
                    draw_top_bar(algorithm_selected)
                    draw_side_panel()
                    draw_grid_container()
                    draw(WIN, grid, ROWS, GRID_SIZE, X_OFFSET, Y_OFFSET)
                
                if algorithm_selected == 1:
                    bfs(draw_func, start, end, DELAY_MS)
                elif algorithm_selected == 2:
                    dfs(draw_func, start, end, DELAY_MS)
                elif algorithm_selected == 3:
                    dijkstra(draw_func, start, end, DELAY_MS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
