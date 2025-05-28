import pygame
import random

pygame.init()

WIDTH, HEIGHT = 690, 690
CELL_SIZE = WIDTH // 3

PLAYER_SYMBOL = "X"
AI_SYMBOL = "O"

BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
BUTTON_COLOR = (0, 255, 0)

BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")
FONT = pygame.font.Font(None, 50)
BUTTON_FONT = pygame.font.Font(None, 30)


class Board:
    def __init__(self):
        self.cells = [["" for _ in range(3)] for _ in range(3)]

        self.x_img = pygame.image.load("krest.png")
        self.o_img = pygame.image.load("krug.png")

        self.x_img = pygame.transform.scale(self.x_img, (CELL_SIZE, CELL_SIZE))
        self.o_img = pygame.transform.scale(self.o_img, (CELL_SIZE, CELL_SIZE))

    def draw(self):
        screen.fill(WHITE_COLOR)
        for i in range(1, 3):
            pygame.draw.line(screen, BLACK_COLOR, (CELL_SIZE * i, 0), (CELL_SIZE * i, HEIGHT), 2)
            pygame.draw.line(screen, BLACK_COLOR, (0, CELL_SIZE * i), (WIDTH, CELL_SIZE * i), 2)
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


class TicTacToeApp:
    def __init__(self):
        self.game = Game()
        self.running = True
        self.reset_button_rect = pygame.Rect(
            (WIDTH - BUTTON_WIDTH) // 2,
            (HEIGHT - BUTTON_HEIGHT) // 2,
            BUTTON_WIDTH,
            BUTTON_HEIGHT
        )
        self.center_click_count = 0
        self.egg_icons_loaded = False

    def run(self):
        while self.running:
            self.handle_events()
            if not self.game.game_over and self.game.turn == "ai":
                self.game.ai_move()
            self.draw()
            pygame.display.flip()
        pygame.quit()

    def draw(self):
        self.game.board.draw()
        if self.game.game_over:
            self.draw_winner()
            self.draw_reset_button()

    def draw_winner(self):
        if self.egg_icons_loaded:
            if self.game.winner == 'Player':
                self.game.winner = 'PEARTO'
            elif self.game.winner == 'AI':
                self.game.winner = 'PEARKU'
        text = FONT.render(
            f"{self.game.winner} Wins!" if self.game.winner != "Tie" else "It's a Tie!",
            True, BLACK_COLOR)
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(text, rect)

    def draw_reset_button(self):
        pygame.draw.rect(screen, BUTTON_COLOR, self.reset_button_rect)
        text = BUTTON_FONT.render("Reset", True, WHITE_COLOR)
        screen.blit(text, text.get_rect(center=self.reset_button_rect.center))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
                if x == 1 and y == 1:
                    self.center_click_count += 1
                    if self.center_click_count >= 39 and not self.egg_icons_loaded:
                        self.load_alternate_icons()
                        print("🎉 Пасхалка активирована! Иконки заменены.")
                else:
                    self.center_click_count = 0

                if self.game.game_over and self.reset_button_rect.collidepoint(event.pos):
                    self.game.reset()
                elif not self.game.game_over and self.game.turn == "player":
                    self.game.player_move(x, y)

    def load_alternate_icons(self):
        self.game.board.x_img = pygame.transform.scale(
            pygame.image.load("pearto.png"), (CELL_SIZE, CELL_SIZE)
        )
        self.game.board.o_img = pygame.transform.scale(
            pygame.image.load("pearku.png"), (CELL_SIZE, CELL_SIZE)
        )
        self.egg_icons_loaded = True


if __name__ == "__main__":
    app = TicTacToeApp()
    app.run()
