import pygame

pygame.init()

WIDTH, HEIGHT = 690, 690
CELL_SIZE = WIDTH // 3

PLAYER_SYMBOL = "X"
AI_SYMBOL = "O"

LINE_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")


class Board:
    def __init__(self):
        self.cells = [
            ["X", "X", "X"],
            ["", "O", ""],
            ["O", "", ""]
        ]

        self.x_img = pygame.image.load("krest.png")
        self.o_img = pygame.image.load("krug.png")
        self.x_img = pygame.transform.scale(self.x_img, (CELL_SIZE, CELL_SIZE))
        self.o_img = pygame.transform.scale(self.o_img, (CELL_SIZE, CELL_SIZE))

    def draw(self):
        screen.fill(BACKGROUND_COLOR)

        for i in range(1, 3):
            pygame.draw.line(screen, LINE_COLOR, (CELL_SIZE * i, 0), (CELL_SIZE * i, HEIGHT), 2)
            pygame.draw.line(screen, LINE_COLOR, (0, CELL_SIZE * i), (WIDTH, CELL_SIZE * i), 2)

        self.draw_symbols()

    def draw_symbols(self):
        for x in range(3):
            for y in range(3):
                symbol = self.cells[x][y]
                pos = (x * CELL_SIZE, y * CELL_SIZE)
                if symbol == PLAYER_SYMBOL:
                    screen.blit(self.x_img, pos)
                elif symbol == AI_SYMBOL:
                    screen.blit(self.o_img, pos)

    def check_winner(self, symbol):
        winning_combinations = [
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(2, 0), (1, 1), (0, 2)],
        ]

        for combo in winning_combinations:
            if all(self.cells[x][y] == symbol for (x, y) in combo):
                return True

        return False


board = Board()
running = True

if board.check_winner(PLAYER_SYMBOL):
    print("Победил игрок!")
elif board.check_winner(AI_SYMBOL):
    print("Победил AI!")
else:
    print("Победителя нет.")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    board.draw()
    pygame.display.flip()

pygame.quit()
