import pygame
import random

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
        self.cells = [["" for _ in range(3)] for _ in range(3)]
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

    def is_full(self):
        return all(cell != "" for row in self.cells for cell in row)

    def make_move(self, x, y, symbol):
        if self.cells[x][y] == "":
            self.cells[x][y] = symbol
            return True
        return False

    def check_winner(self, symbol):
        winning_combinations = [
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(2, 0), (1, 1), (0, 2)]
        ]
        for combo in winning_combinations:
            if all(self.cells[x][y] == symbol for (x, y) in combo):
                return True
        return False

    def reset(self):
        self.cells = [["" for _ in range(3)] for _ in range(3)]


class Game:
    def __init__(self):
        self.board = Board()
        self.turn = "player"
        self.winner = None
        self.game_over = False

    def player_move(self, x, y):
        if self.board.make_move(x, y, PLAYER_SYMBOL):
            self.check_game_state()
            self.turn = "ai"

    def ai_move(self):
        empty = [(x, y) for x in range(3) for y in range(3) if self.board.cells[x][y] == ""]
        if empty:
            x, y = random.choice(empty)
            self.board.make_move(x, y, AI_SYMBOL)
            self.check_game_state()
            self.turn = "player"

    def check_game_state(self):
        if self.board.check_winner(PLAYER_SYMBOL):
            self.winner = "Player"
            self.game_over = True
        elif self.board.check_winner(AI_SYMBOL):
            self.winner = "AI"
            self.game_over = True
        elif self.board.is_full():
            self.winner = "Tie"
            self.game_over = True

    def reset(self):
        self.board.reset()
        self.turn = "player"
        self.winner = None
        self.game_over = False

game = Game()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game.game_over and game.turn == "player":
                x, y = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
                game.player_move(x, y)

    if not game.game_over and game.turn == "ai":
        game.ai_move()
    if game.game_over:
        if game.winner == "Player":
            print("Победил игрок!")
        elif game.winner == "AI":
            print("Победил AI!")
        elif game.winner == "Tie":
            print("Ничья!")
        else:
            print("Победителя нет.")
        running = False
    game.board.draw()
    pygame.display.flip()

pygame.quit()
