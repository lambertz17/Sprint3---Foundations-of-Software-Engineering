
import unittest
from Game import ManualGame


class TestManualGame(unittest.TestCase):

    def setUp(self):
        # Create a new manual game before each test
        self.game = ManualGame(5, "English")

    def test_manual_game_creation(self):
        # Verify the correct board settings
        self.assertEqual(self.game.board.size, 5)
        self.assertEqual(self.game.board.board_type, "English")

    def test_valid_manual_move(self):
        # Create a controlled board with one valid jump
        self.game.board.cells = [
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
            [1, 1, 0, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1]
        ]

        # Move a peg over another peg into an empty hole
        result = self.game.make_moves(2, 0, 2, 2)

        self.assertTrue(result)
        self.assertEqual(self.game.board.cells[2][0], 0)
        self.assertEqual(self.game.board.cells[2][1], 0)
        self.assertEqual(self.game.board.cells[2][2], 1)

    def test_invalid_manual_move(self):
        # Attempt to move onto the same position
        result = self.game.make_moves(2, 2, 2, 2)

        # Invalid moves must be rejected
        self.assertFalse(result)

    def test_manual_game_over(self):
        # Create a board with no possible moves
        self.game.board.cells = [
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, 1, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1]
        ]

        self.assertTrue(self.game.is_game_over())
        self.assertTrue(self.game.is_game_won())


if __name__ == "__main__":
    unittest.main()
