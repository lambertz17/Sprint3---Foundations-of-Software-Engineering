
from Board import Board

# Board types and sizes to test
board_types = ["English", "Diamond", "Hexagon"]
board_sizes = [5, 7, 9]

# Test every board type with every size
for board_type in board_types:
    for size in board_sizes:

        print(f"\n{board_type} Board - Size {size}")
        print("-" * 30)

        # Create the board
        board = Board(size, board_type)

        # Display the board in the terminal
        for row in board.cells:
            print(" ".join(
                "." if cell == -1 else str(cell)
                for cell in row
            ))

        print()
