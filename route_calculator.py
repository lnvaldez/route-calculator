
import pygame

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (170, 170, 170)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Square:
    def __init__(self, x, y, size, color):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.default_color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def handle_click(self):
        if self.color == self.default_color:
            self.color = RED
        else:
            self.color = self.default_color

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

# Set up display
screen = pygame.display.set_mode((1080, 720))
pygame.display.set_caption("Route Calculator")

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
        screen.fill((0, 0, 0))
    elif page == 2:
        screen.fill((255, 255, 0))

# Create grid
def create_grid(rows, cols, size, margin):
    grid = []
    for row in range(rows):
        grid_row = []
        for col in range(cols):
            x = col * (size + margin) + margin
            y = row * (size + margin) + margin
            square = Square(x, y, size, BLUE)
            grid_row.append(square)
        grid.append(grid_row)
    return grid

def draw_grid(grid, screen):
    for row in grid:
        for square in row:
            square.draw(screen)

# Create buttons
button1 = Button(100, 600, 300, 100, 'Tutorial', GRAY, LIGHT_GRAY, BLACK)
button2 = Button(400, 600, 300, 100, 'Design', GRAY, LIGHT_GRAY, BLACK)
button3 = Button(700, 600, 300, 100, 'Solution', GRAY, LIGHT_GRAY, BLACK)

# Grid parameters
grid_size = 100
grid_margin = 5
rows = (screen.get_height() - 150) // (grid_size + grid_margin)
cols = screen.get_width() // (grid_size + grid_margin)
grid = create_grid(rows, cols, grid_size, grid_margin)

# Main loop
running = True
while running:
    screen.fill(bg_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for row in grid:
                for square in row:
                    if square.rect.collidepoint(event.pos):
                        square.handle_click()
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

    if page == 1:
        draw_grid(grid, screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()