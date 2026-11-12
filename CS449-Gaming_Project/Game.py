from Board import Board

class Game:

    
    def __init__(self, size, board_type, randomize_board=False):

        # Create the selected board
        self.board = Board(size, board_type)

        # Randomize the starting hole if requested
        if randomize_board:
            self.board.randomize_empty_hole()

        # Save the starting board for recording
        self.initial_board = [
            row.copy() for row in self.board.cells
        ]

        # Track successful moves
        self.move_history = []


    def new_game(self, size, board_type):
        self.board = Board(size, board_type)

        # Save the new starting board
        self.initial_board = [
            row.copy() for row in self.board.cells
        ]

        # Clear moves from the previous game
        self.move_history = []

    def is_valid_move(self, start_row, start_col, end_row, end_col):

    # Validation Tests
        if not self.board.is_valid_position(start_row, start_col):
            return False

        if not self.board.is_valid_position(end_row, end_col):
            return False

        if self.board.cells[start_row][start_col] != 1:
            return False

        if self.board.cells[end_row][end_col] != 0:
            return False


        row_difference = end_row - start_row
        col_difference = end_col - start_col

        if (row_difference, col_difference) not in self.get_move_directions():
            return False

        middle_row = (start_row + end_row) // 2
        middle_col = (start_col + end_col) // 2

        if self.board.cells[middle_row][middle_col] != 1:
            return False

        return True

    def get_move_directions(self):
        return [
        (-2, 0),   # Up
        (2, 0),    # Down
        (0, -2),   # Left
        (0, 2),    # Right
        (-2, -2),  # Up-left
        (-2, 2),   # Up-right
        (2, -2),   # Down-left
        (2, 2)     # Down-right
    ]
    
    
    def make_moves(self, start_row, start_col, end_row, end_col):

        # Validate the move before making changes
        if not self.is_valid_move(
            start_row, start_col, end_row, end_col
        ):
            return False

        # Find the peg being jumped over
        middle_row = (start_row + end_row) // 2
        middle_col = (start_col + end_col) // 2

        # Remove the starting peg
        self.board.cells[start_row][start_col] = 0

        # Remove the jumped peg
        self.board.cells[middle_row][middle_col] = 0

        # Place the peg in its destination
        self.board.cells[end_row][end_col] = 1

        # Record the successful move
        self.move_history.append(
            (start_row, start_col, end_row, end_col)
        )

        return True


    def is_game_over(self):
        return len(self.available_moves()) == 0

    def available_moves(self):
        moves = []

        for row in range(self.board.size):
            for column in range(self.board.size):
                if self.board.cells[row][column] != 1:
                    continue

                directions = self.get_move_directions()

                for row_change, column_change in directions:
                    end_row = row + row_change
                    end_col = column + column_change

                    if self.is_valid_move(row, column, end_row, end_col):
                        moves.append((row, column, end_row, end_col))

        return moves

    def is_game_won(self):
        peg_count = 0

        for row in self.board.cells:
            for cell in row:
                if cell == 1:
                    peg_count += 1

        return peg_count == 1

class AutomatedGame(Game):
    def autoplay_step(self):
        moves = self.available_moves()

        if not moves:
            return False

        start_row, start_col, end_row, end_col = moves[0]

        return self.make_moves(start_row, start_col, end_row, end_col)

class ManualGame(Game):
    pass