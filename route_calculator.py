import pygame

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (170, 170, 170)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

class Square:
    def __init__(self, x, y, size, color):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.default_color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 1)

    def handle_click(self, sq_type):
        if sq_type == 1:
            self.color = RED
        elif sq_type == 2:
            self.color = WHITE
        elif sq_type == 3:
            self.color = YELLOW
        elif sq_type == 4:
            self.color = BLUE
        elif sq_type == 5:
            self.color = LIGHT_GRAY
        else:
            self.color = GREEN

            
class StaticSquare:
    def __init__(self, x, y, size, color, label):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.default_color = color
        self.label = label

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 1)
        
        font = pygame.font.Font(None, 24)
        label_surf = font.render(self.label, True, BLACK)
        label_rect = label_surf.get_rect(midleft=(self.rect.right + 10, self.rect.centery))
        screen.blit(label_surf, label_rect)

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 1)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# Initialize Pygame
pygame.init()

WIDTH = 1080
HEIGHT = 740

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Route Calculator")

font = pygame.font.Font(None, 36)

# Set up clock
clock = pygame.time.Clock()

# Set up background color
bg_color = WHITE

# Page state
page = 0

def switchScreen(screen, page):
    if page == 0:
        screen.fill((255, 255, 255))
    elif page == 1:
        screen.fill((255, 255, 255))
    elif page == 2:
        screen.fill((255, 255, 255))

# Create grid
def create_grid(rows, cols, size, margin, start_x, start_y):
    grid = []
    for row in range(rows):
        grid_row = []
        for col in range(cols):
            x = start_x + col * (size + margin)
            y = start_y + row * (size + margin)
            square = Square(x, y, size, WHITE)
            grid_row.append(square)
        grid.append(grid_row)
    return grid

def draw_grid(grid, screen, start_x, start_y, size, margin):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            square = grid[row][col]
            square.draw(screen)
    
    # Draw row labels
    for row in range(len(grid)):
        label = font.render(str(row), True, BLACK)
        label_rect = label.get_rect(center=(start_x - margin, start_y + row * (size + margin) + size // 2))
        screen.blit(label, label_rect)
    
    # Draw column labels
    for col in range(len(grid[0])):
        label = font.render(str(col), True, BLACK)  # Convert column index to letters (A, B, C, etc.)
        label_rect = label.get_rect(center=(start_x + col * (size + margin) + size // 2, start_y - margin))
        screen.blit(label, label_rect)

# Create squares for page 0
sq_size = 50
sq_margin = 20
start_x = 100
start_y = 105

sq1 = StaticSquare(start_x, start_y, sq_size, RED, "Press '1' and click on square to draw 'Starting Point'")
sq2 = StaticSquare(start_x, start_y + sq_size + sq_margin, sq_size, WHITE, "Press '2' and click on square to draw 'Path'")
sq3 = StaticSquare(start_x, start_y + 2 * (sq_size + sq_margin), sq_size, YELLOW, "Press '3' and click on square to draw 'Roadwork/Construction'")
sq4 = StaticSquare(start_x, start_y + 3 * (sq_size + sq_margin), sq_size, BLUE, "Press '4' and click on square to draw 'Body Of Water'")
sq5 = StaticSquare(start_x, start_y + 4 * (sq_size + sq_margin), sq_size, GRAY, "Press '5' and click on square to draw 'Building'")
sq6 = StaticSquare(start_x, start_y + 5 * (sq_size + sq_margin), sq_size, GREEN, "Press '6' and click on square to draw 'End Point'")

# Create buttons
button1 = Button(100, 600, 300, 100, 'Tutorial', GRAY, LIGHT_GRAY, BLACK)
button2 = Button(400, 600, 300, 100, 'Design', GRAY, LIGHT_GRAY, BLACK)
button3 = Button(700, 600, 300, 100, 'Solution', GRAY, LIGHT_GRAY, BLACK)

# Grid parameters
grid_size = 100
grid_margin = 5
button_height = 100
rows = (screen.get_height() - button_height - 50) // (grid_size + grid_margin)
cols = screen.get_width() // (grid_size + grid_margin)
start_x = (screen.get_width() - (cols * (grid_size + grid_margin) - grid_margin)) // 2
start_y = (screen.get_height() - button_height - 50 - (rows * (grid_size + grid_margin) - grid_margin)) // 2
grid = create_grid(rows, cols, grid_size, grid_margin, start_x + 10, start_y + 10)

# Main loop
running = True
color_type = 0
while running:
    screen.fill(bg_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for row in grid:
                for square in row:
                    if square.rect.collidepoint(event.pos):
                        square.handle_click(color_type)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                color_type = 1
            elif event.key == pygame.K_2:
                color_type = 2
            elif event.key == pygame.K_3:
                color_type = 3
            elif event.key == pygame.K_4:
                color_type = 4
            elif event.key == pygame.K_5:
                color_type = 5
            elif event.key == pygame.K_6:
                color_type = 6
        if button1.is_clicked(event):
            page = 0
        elif button2.is_clicked(event):
            page = 1
        elif button3.is_clicked(event):
            page = 2

    switchScreen(screen, page)
    button1.draw(screen)
    button2.draw(screen)
    button3.draw(screen)

    if page == 0:
        font = pygame.font.Font(None, 36)
        tut_text = font.render('Tutorial', True, BLACK)
        tut_text_rect = tut_text.get_rect(center=(350, 50)) 
        inp_text = font.render('Enter grid dimensions', True, BLACK)
        inp_text_rect = tut_text.get_rect(center=(750, 50)) 
        screen.blit(tut_text, tut_text_rect) 
        screen.blit(inp_text, inp_text_rect)

        sq1.draw(screen)
        sq2.draw(screen)
        sq3.draw(screen)
        sq4.draw(screen)
        sq5.draw(screen)
        sq6.draw(screen)

    if page == 1 or page == 2:
        draw_grid(grid, screen, start_x, start_y, grid_size, grid_margin)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
