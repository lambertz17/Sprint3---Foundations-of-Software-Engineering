
import json


class GameRecording:

    @staticmethod
    def save_game(game, filename):

        # Collect the game information
        game_data = {
            "board_type": game.board.board_type,
            "board_size": game.board.size,
            "initial_board": game.initial_board,
            "moves": game.move_history
        }

        # Write the game information to a text file
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(game_data, file, indent=4)

    @staticmethod
    def load_game(filename):

        # Read the saved game information
        with open(filename, "r", encoding="utf-8") as file:
            game_data = json.load(file)

        # Check that the required information exists
        required_fields = [
            "board_type",
            "board_size",
            "initial_board",
            "moves"
        ]

        for field in required_fields:
            if field not in game_data:
                raise ValueError(
                    f"Recording is missing: {field}"
                )

        return game_data
