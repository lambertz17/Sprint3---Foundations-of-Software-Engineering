import unittest
from Game import Game

class TestGame(unittest.TestCase):

# Test 1: Game initalizes with the correct board
    def test_game_initialization(self):
        game = Game(7, "English")

        self.assertEqual(game.board.size, 7)
        self.assertEqual(game.board.board_type, "English")
        self.assertEqual(game.board.cells[3][3], 0)

# Test 2: New game resets the board
    def test_new_game_resets_board(self):
        game = Game(7, "English")

        game.make_moves(3, 1, 3, 3)

        game.new_game(7, "English")

        self.assertEqual(game.board.cells[3][1], 1)
        self.assertEqual(game.board.cells[3][2], 1)
        self.assertEqual(game.board.cells[3][3], 0)

# Test 3: New game can change board type
    def test_new_game_changes_board_type(self):
        game = Game(7, "English")

        game.new_game(7, "Diamond")

        self.assertEqual(game.board.board_type, "Diamond")
        self.assertEqual(game.board.size, 7)

# Test 4: Recognize valid move
    def test_valid_move(self):
        game = Game(7, "English")

        result = game.is_valid_move(3, 1, 3, 3)

        self.assertTrue(result)

# Test 5: Reject invalid starting position
    def test_invalid_start_position(self):
        game = Game(7, "English")

        result = game.is_valid_move(-1, 3, 1, 3)

        self.assertFalse(result)

# Test 6: Reject invalid destination
    def test_invalid_destination(self):
        game = Game(7, "English")

        result = game.is_valid_move(0, 0, 0, 2)

        self.assertFalse(result)

#Test 7: Reject invalid movement distance
    def test_invalid_move_distance(self):
        game = Game(7, "English")

        result = game.is_valid_move(3, 2, 3, 3)

        self.assertFalse(result)

# Test 8: Making a move updates the board
    def test_make_move(self):
        game = Game(7, "English")

        result = game.make_moves(3, 1, 3, 3)

        self.assertTrue(result)
        self.assertEqual(game.board.cells[3][1], 0)
        self.assertEqual(game.board.cells[3][2], 0)
        self.assertEqual(game.board.cells[3][3], 1)

# Test 9: Invalid moves do not change the board
    def test_invalid_does_not_change_board(self):
        game = Game(7, "English")

        original_board = [row.copy() for row in game.board.cells]

        result = game.make_moves(3, 2, 3, 3)

        self.assertFalse(result)
        self.assertEqual(game.board.cells, original_board)

# Test 10: Game over when no moves remain
    def test_game_over(self):
        game = Game(7, "English")

        for row in range(game.board.size):
            for column in range(game.board.size):
                if game.board.is_valid_position(row, column):
                    game.board.cells[row][column] = 0

        game.board.cells[3][3] = 1

        self.assertTrue(game.is_game_over())

# Test 11: Test hexagon diagonal move
    def test_hexagon_diagonal_move(self):
        game = Game(7, "Hexagon")

        result = game.is_valid_move(5, 1,3, 3)

        self.assertTrue(result)

# Test 12: Game is won with one peg remaining
    def test_game_won(self):
        game = Game(7, "English")

        for row in range (game.board.size):
            for col in range(game.board.size):
                if game.board.is_valid_position(row, col):
                    game.board.cells[row][col] = 0

        game.board.cells[3][3] = 1

        self.assertTrue(game.is_game_won())

# Test 13: Game is not won with multiple pegs
    def test_game_not_won(self):
        game = Game(7, "English")

        self.assertFalse(game.is_game_won())
if __name__ == "__main__":
    unittest.main()