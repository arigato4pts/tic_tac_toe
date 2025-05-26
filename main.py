import pygame

pygame.init()

WIDTH, HEIGHT = 690, 690
CELL_SIZE = WIDTH // 3

LINE_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

class Board:
    def __init__(self):
        self.cells = [["" for _ in range(3)] for _ in range(3)]

    def draw(self):
        screen.fill(BACKGROUND_COLOR)
        for i in range(1, 3):
            pygame.draw.line(screen, LINE_COLOR, (CELL_SIZE * i, 0), (CELL_SIZE * i, HEIGHT), 2)
            pygame.draw.line(screen, LINE_COLOR, (0, CELL_SIZE * i), (WIDTH, CELL_SIZE * i), 2)

board = Board()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    board.draw()
    pygame.display.flip()

pygame.quit()
