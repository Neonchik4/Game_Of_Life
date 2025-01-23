import unittest
from main import Board


class TestBoard(unittest.TestCase):
    def setUp(self):
        """Инициализация игрового поля для тестов"""
        self.board = Board(5, 5)

    def test_initial_state(self):
        """Тест начального состояния игрового поля"""
        for row in self.board.board:
            self.assertTrue(all(cell == 0 for cell in row), "Все клетки должны быть мёртвы в начале")

    def test_on_click(self):
        """Тест изменения состояния клетки при клике"""
        self.board.on_click((2, 2))
        self.assertEqual(self.board.board[2][2], 1, "Клетка должна стать живой после клика")
        self.board.on_click((2, 2))
        self.assertEqual(self.board.board[2][2], 0, "Клетка должна стать мёртвой после второго клика")

    def test_get_cell(self):
        """Тест определения клетки по координатам мыши"""
        self.board.set_view(10, 10, 20)
        self.assertEqual(self.board.get_cell((30, 30)), (1, 1), "Клетка должна быть (1, 1)")
        self.assertIsNone(self.board.get_cell((5, 5)), "Клик вне поля должен возвращать None")

    def test_count_live_neighbors(self):
        """Тест подсчёта живых соседей"""
        self.board.board[1][1] = 1
        self.board.board[1][2] = 1
        self.board.board[2][1] = 1
        self.assertEqual(self.board.count_live_neighbors(2, 2), 3, "Должно быть 3 живых соседа")

    def test_update(self):
        """Тест обновления состояния игрового поля"""
        self.board.board[1][1] = 1
        self.board.board[1][2] = 1
        self.board.board[2][1] = 1
        self.board.update()
        self.assertEqual(self.board.board[2][2], 1, "Клетка (2, 2) должна ожить")

if __name__ == "__main__":
    unittest.main()
