import pygame
import time


class Board:
    def __init__(self, width, height):
        """Инициализация игрового поля с заданной шириной и высотой"""
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def render(self, screen):
        """Отображение игрового поля на экране"""
        colors = [pygame.Color("black"), pygame.Color("green")]  # цвета
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, colors[self.board[y][x]], (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size))
                pygame.draw.rect(screen, pygame.Color("white"), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size), 1)

    def set_view(self, left, top, cell_size):
        """Устанавливает параметры отображения поля"""
        # Отступы слева, сверху и размер клетки
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def on_click(self, cell):
        """Обрабатывает клик по клетке, меняя её состояние"""
        i, j = cell
        self.board[j][i] = (self.board[j][i] + 1) % 2

    def get_cell(self, mouse_pos):
        """Определяет, на какую клетку нажали мышью"""
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        """Обрабатывает событие клика мышью"""
        cell = self.get_cell(mouse_pos)
        if cell:

            self.on_click(cell)

    def update(self):
        """Обновляет состояние поля"""
        new_board = [[0] * self.width for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                live_neighbors = self.count_live_neighbors(x, y)
                if self.board[y][x] == 1:
                    if live_neighbors == 2 or live_neighbors == 3:
                        new_board[y][x] = 1
                else:
                    if live_neighbors == 3:
                        new_board[y][x] = 1
        self.board = new_board

    def count_live_neighbors(self, x, y):
        """Считает количество живых соседей вокруг клетки с координатами (x, y)"""
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = (x + dx) % self.width, (y + dy) % self.height
                count += self.board[ny][nx]
        return count

if __name__ == "__main__":
    pygame.init()
    size = 800, 800
    screen = pygame.display.set_mode(size)

    # создаем поле
    board = Board(40, 40)
    board.set_view(0, 0, 20)

    game_running = False
    running = True

    # главный цикл
    while running:
        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not game_running:
                board.get_click(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_running = not game_running

        if game_running:
            board.update()
            time.sleep(0.2)

        screen.fill((0, 0, 0))  # Очистка экрана
        board.render(screen)  # Отображение игрового поля
        pygame.display.flip()  # Обновление экрана

    pygame.quit()
