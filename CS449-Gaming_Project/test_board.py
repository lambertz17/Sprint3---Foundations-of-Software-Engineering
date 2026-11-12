import unittest
from Board import Board

class TestBoard(unittest.TestCase):

# Test 1: Test English board size
    def test_english_board_size(self):
        board = Board(7, "English")

        self.assertEqual(len(board.cells), 7)

        for row in board.cells:
            self.assertEqual(len(row), 7)

# Test 2: Test Diamond board size
    def test_diamond_board_size(self):
        board = Board(7, "Diamond")

        self.assertEqual(len(board.cells), 7)

        for row in board.cells:
            self.assertEqual(len(row), 7)

# Test 3: Test Hexagon board size
    def test_hexagon_board_size(self):
        board = Board(7, "Hexagon")

        self.assertEqual(len(board.cells), 7)

        for row in board.cells:
            self.assertEqual(len(row), 7)

# Test 4: Center is empty for all board types
    def test_empty_center(self):
        for board_type in ["English", "Diamond", "Hexagon"]:
            with self.subTest(board_type=board_type):
                board = Board(7, board_type)

                center = board.size // 2

                self.assertEqual(
                    board.cells[center][center], 0
                )

# Test 5: English board shape
    def test_english_board_shape(self):
        board = Board(7, "English")

        self.assertEqual(board.cells[0][0], -1)
        self.assertEqual(board.cells[0][3], 1)
        self.assertEqual(board.cells[3][0], 1)
        self.assertEqual(board.cells[6][6], -1)

# Test 6: Diamond board shape
    def test_diamond_board_shape(self):
        board = Board(7, "Diamond")

        self.assertEqual(board.cells[0][0], -1)
        self.assertEqual(board.cells[0][3], 1)
        self.assertEqual(board.cells[1][2], 1)
        self.assertEqual(board.cells[1][1], -1)

# Test 7: Hexagon board shape
    def test_hexagon_board_shape(self):
       board = Board(7, "Hexagon")

       self.assertEqual(board.cells[0][0], -1)
       self.assertEqual(board.cells[0][3], 1)
       self.assertEqual(board.cells[0][6], 1)
       self.assertEqual(board.cells[6][0], 1)
       self.assertEqual(board.cells[6][6], -1)

# Test 8: Valid board positions
    def test_valid_positions(self):
        board = Board(7, "English")

        self.assertTrue(board.is_valid_position(3,3))
        self.assertTrue(board.is_valid_position(0,3))
        self.assertTrue(board.is_valid_position(3,0))

# Test 9: Invalid board positions
    def test_invalid_positions(self):
        board = Board(7, "English")

        self.assertFalse(board.is_valid_position(0,0))
        self.assertFalse(board.is_valid_position(6,6))
        self.assertFalse(board.is_valid_position(-1, 3))
        self.assertFalse(board.is_valid_position(7,3))

    def test_invalid_board_type(self):
        with self.assertRaises(ValueError):
            Board(7, "Circle")


if __name__ == "__main__":
    unittest.main()