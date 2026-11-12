
import unittest
from Game import AutomatedGame


class TestAutomatedGame(unittest.TestCase):

    def setUp(self):
        # Create a new automated game before each test
        self.game = AutomatedGame(5, "English")

    def test_automated_game_creation(self):
        # Verify the correct board settings
        self.assertEqual(self.game.board.size, 5)
        self.assertEqual(self.game.board.board_type, "English")

    def test_autoplay_makes_valid_move(self):
        # Find the first available move
        moves = self.game.available_moves()

        self.assertGreater(len(moves), 0)

        # Perform one automated move
        result = self.game.autoplay_step()

        self.assertTrue(result)

    def test_autoplay_reduces_peg_count(self):
        # Count pegs before the automated move
        before = sum(
            row.count(1) for row in self.game.board.cells
        )

        self.game.autoplay_step()

        # Count pegs after the automated move
        after = sum(
            row.count(1) for row in self.game.board.cells
        )

        # Every successful move removes one peg
        self.assertEqual(after, before - 1)

    def test_autoplay_stops_when_no_moves_remain(self):
        # Create a board with only one peg
        self.game.board.cells = [
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, 1, -1, -1],
            [-1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1]
        ]

        # Automated mode should not make another move
        result = self.game.autoplay_step()

        self.assertFalse(result)
        self.assertTrue(self.game.is_game_over())


if __name__ == "__main__":
    unittest.main()
