import random

class Board: 

    def __init__(self, size, board_type):
        self.size = size
        self.board_type = board_type

        if size not in (5, 7, 9):
            raise ValueError("Invalid board size")

        self.cells = self.create_board()

    def create_board(self):
        if self.board_type == "English":
            return self.create_english_board()

        elif self.board_type == "Diamond":
            return self.create_diamond_board()

        elif self.board_type == "Hexagon":
            return self.create_hexagon_board()

        else:
            raise ValueError("Invalid board type")

    def create_english_board(self):
        board = []
        center = self.size // 2
        arm_width = 1 if self.size == 5 else 3

        middle_start = (self.size - arm_width) // 2
        middle_end = middle_start + arm_width
        
        for row in range (self.size):
            new_row = []

            for column in range(self.size):

                if row == center and column == center:
                    new_row.append(0)

                elif(middle_start <= row < middle_end or
                     middle_start <= column < middle_end):
                    new_row.append(1)

                else:
                    new_row.append(-1)

            board.append(new_row)

        return board

    def create_diamond_board(self):
        board = []
        center = self.size // 2

        for row in range(self.size):
            current_row = []

            for column in range(self.size):

                distance = abs(row - center) + abs(column - center)

                if row == center and column == center:
                    current_row.append(0)

                elif distance <= center:
                    current_row.append(1)

                else: 
                    current_row.append(-1)

            board.append(current_row)

        return board


    def create_hexagon_board(self):
        board = []
        center = self.size // 2

        for row in range(self.size):
            current_row = []

            for column in range(self.size):

                if row < center:
                    start_column = center - row
                else:
                    start_column = 0

                if row <= center:
                    end_column = self.size
                else:
                    end_column = self.size - (row - center)

                if row == center and column == center:
                    current_row.append(0)

                elif start_column <= column < end_column:
                    current_row.append(1)

                else: current_row.append(-1)

            board.append(current_row)

        return board
                

    def is_valid_position(self, row, column):
        if 0 <= row < self.size and 0 <= column < self.size:
            return self.cells[row][column] != -1
        
        return False

    
    def randomize_empty_hole(self):

        # Find the current empty starting hole
        for row in range(self.size):
            for column in range(self.size):
                if self.cells[row][column] == 0:
                    self.cells[row][column] = 1

        # Find all valid peg positions
        valid_positions = []

        for row in range(self.size):
            for column in range(self.size):
                if self.cells[row][column] == 1:
                    valid_positions.append((row, column))

        # Randomly choose the new empty hole
        empty_row, empty_col = random.choice(valid_positions)

        # Remove the peg at that position
        self.cells[empty_row][empty_col] = 0
