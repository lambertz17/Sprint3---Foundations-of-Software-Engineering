
import tkinter as tk

from Game import ManualGame, AutomatedGame
from SetupScreen import SetupScreen
from GameScreen import GameScreen


class SolitaireGUI:

    def __init__(self, root):

        # Store the main window
        self.root = root

        # Configure the main window
        self.root.title("Peg Solitaire")
        self.root.geometry("950x850")
        self.root.configure(bg="#171B22")

        # Track the currently displayed screen
        self.current_screen = None

        # Display the setup screen first
        self.show_setup_screen()

    
    def show_setup_screen(self):

        # Stop autoplay if a game is currently running
        if isinstance(self.current_screen, GameScreen):
            self.current_screen.stop_autoplay()

        # Remove the current screen
        if self.current_screen is not None:
            self.current_screen.destroy()

        # Create the setup screen with both callbacks
        self.current_screen = SetupScreen(
            self.root,
            self.start_game,
            self.replay_game
        )

        self.current_screen.pack(
            fill="both",
            expand=True
        )


    
    def start_game(self, mode, board_type, size, randomize_board=False):

        # Create the selected game mode
        if mode == "Automated":
            game = AutomatedGame(
                size, board_type, randomize_board
            )
        else:
            game = ManualGame(
                size, board_type, randomize_board
            )

        # Remove the setup screen
        self.current_screen.destroy()

        # Display the game screen
        self.current_screen = GameScreen(
            self.root,
            game,
            self.show_setup_screen
        )

        self.current_screen.pack(fill="both", expand=True)


    
    def replay_game(self, game_data):

        # Get the recorded board settings
        board_type = game_data["board_type"]
        size = game_data["board_size"]

        # Create a game to replay the saved moves
        game = ManualGame(size, board_type)

        # Restore the exact starting board
        game.board.cells = [
            row.copy() for row in game_data["initial_board"]
        ]

        # Save the starting board for replay
        game.initial_board = [
            row.copy() for row in game.board.cells
        ]

        # Get the recorded moves
        recorded_moves = game_data["moves"]

        # Remove the setup screen
        if self.current_screen is not None:
            self.current_screen.destroy()

        # Create the game screen
        self.current_screen = GameScreen(
            self.root,
            game,
            self.show_setup_screen
        )

        self.current_screen.pack(
            fill="both",
            expand=True
        )

        # Start replaying the recorded moves
        self.current_screen.start_replay(recorded_moves)



