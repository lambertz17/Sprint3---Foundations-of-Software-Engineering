import tkinter as tk
from tkinter import messagebox

from Game import AutomatedGame
from Graphics import BoardGraphics
from tkinter import filedialog
from Recording import GameRecording

class GameScreen(tk.Frame):

    def __init__(self, parent, game, on_new_game):
        super().__init__(parent, bg="#171B22")

        # Store the current game
        self.game = game

        # Callback to return to the setup screen
        self.on_new_game = on_new_game

        # Track the selected peg
        self.selected_peg = None

        # Track whether the game has ended
        self.game_finished = False

        # Automated gameplay settings
        self.autoplay_job = None
        self.autoplay_running = False

        # Replay settings
        self.replay_moves = []
        self.replay_index = 0
        self.replay_running = False
        self.replay_job = None
        self.is_replay = False

        # Build the gameplay interface
        self.create_widgets()

        # Connect the board graphics
        self.graphics = BoardGraphics(self.canvas)

        # Draw the starting board
        self.draw_board()

        # Start automated games automatically
        if isinstance(self.game, AutomatedGame):
            self.autoplay_job = self.after(
                100,
                self.start_autoplay
            )
        else:
            self.update_status("Select a peg to begin.")

    
    def create_widgets(self):

        # Game title
        tk.Label(
            self,
            text="PEG SOLITAIRE",
            font=("Arial", 26, "bold"),
            bg="#171B22",
            fg="#E6E6E6"
        ).pack(pady=(20, 10))

        # Display selected game settings
        mode = (
            "Automated"
            if isinstance(self.game, AutomatedGame)
            else "Manual"
        )

        settings_text = (
            f"{mode} Play | "
            f"{self.game.board.board_type} Board | "
            f"{self.game.board.size} x {self.game.board.size}"
        )

        tk.Label(
            self,
            text=settings_text,
            font=("Arial", 12),
            bg="#171B22",
            fg="#AAB5C0"
        ).pack(pady=5)

        # Board canvas
        self.canvas = tk.Canvas(
            self,
            width=850,
            height=600,
            bg="#171B22",
            highlightthickness=0
        )
        self.canvas.pack(pady=10)

        # Listen for manual moves
        self.canvas.bind(
            "<Button-1>",
            self.handle_click
        )

        # Remaining peg counter
        self.peg_count_label = tk.Label(
            self,
            text="",
            font=("Arial", 14, "bold"),
            bg="#171B22",
            fg="#DCE5ED"
        )
        self.peg_count_label.pack(pady=5)

        # Status message
        self.status_label = tk.Label(
            self,
            text="",
            font=("Arial", 11),
            bg="#171B22",
            fg="#AAB5C0"
        )
        self.status_label.pack(pady=5)


        
        # Container for game control buttons
        control_frame = tk.Frame(
            self,
            bg="#242A33",
            highlightbackground="#825536",
            highlightthickness=2,
            padx=15,
            pady=12
        )

        # Position controls in the bottom-right corner
        control_frame.place(
            relx=1.0,
            rely=1.0,
            anchor="se",
            x=-20,
            y=-20
        )

        
        # SAVE GAME button
        self.save_button = tk.Button(
            control_frame,
            text="SAVE GAME",
            font=("Arial", 12, "bold"),
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            disabledforeground="#AAB5C0",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.save_game,
            state="disabled"
        )

        self.save_button.pack(fill="x", pady=(0, 10))


        # MAIN MENU button
        tk.Button(
            control_frame,
            text="MAIN MENU",
            font=("Arial", 12, "bold"),
            bg="#825536",
            fg="white",
            activebackground="#A56B42",
            activeforeground="white",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.main_menu
        ).pack(fill="x", pady=(0, 10))

        # EXIT button
        tk.Button(
            control_frame,
            text="EXIT",
            font=("Arial", 12, "bold"),
            bg="#9B3030",
            fg="white",
            activebackground="#B84040",
            activeforeground="white",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.exit_game
        ).pack(fill="x")
    
    def return_to_setup(self):

        # Stop automated gameplay
        self.stop_autoplay()

        # Stop replay playback
        self.stop_replay()

        # Return to the setup screen
        self.on_new_game()

    def stop_autoplay(self):

        # Cancel any scheduled automated move
        if self.autoplay_job is not None:
            self.after_cancel(self.autoplay_job)
            self.autoplay_job = None

        self.autoplay_running = False

    def draw_board(self):

        # Draw the current board
        self.graphics.draw_board(
            self.game.board,
            self.selected_peg
        )

        # Update the peg counter
        self.update_peg_count()

    def update_peg_count(self):

        # Count all remaining pegs
        peg_count = sum(
            cell == 1
            for row in self.game.board.cells
            for cell in row
        )

        self.peg_count_label.config(
            text=f"Pegs Remaining: {peg_count}"
        )
     
    def update_status(self, message):
        self.status_label.config(text=message)

    def handle_click(self, event):

        if (
            self.game_finished
            or self.is_replay
            or isinstance(self.game, AutomatedGame)
        ):
            return

        # Determine which board position was clicked
        clicked_cell = self.graphics.find_clicked_cell(
            event.x,
            event.y
        )

        # Ignore clicks outside the board
        if clicked_cell is None:
            return

        row, col = clicked_cell
        cell_value = self.game.board.cells[row][col]

        # First click: select a peg
        if self.selected_peg is None:

            if cell_value == 1:
                self.selected_peg = (row, col)
                self.draw_board()

                self.update_status(
                    f"Selected peg at ({row}, {col})."
                )

            return

        # Clicking the same peg deselects it
        if self.selected_peg == (row, col):

            self.selected_peg = None
            self.draw_board()

            self.update_status("Peg deselected.")
            return

        # Clicking another peg changes selection
        if cell_value == 1:

            self.selected_peg = (row, col)
            self.draw_board()

            self.update_status(
                f"Selected peg at ({row}, {col})."
            )
            return

        # Attempt to move into an empty hole
        start_row, start_col = self.selected_peg

        move_successful = self.game.make_moves(
            start_row,
            start_col,
            row,
            col
        )

        # Clear the selected peg
        self.selected_peg = None

        # Redraw the board
        self.draw_board()

        if not move_successful:

            self.update_status(
                "Invalid move. Try again."
            )
            return

        self.update_status(
            "Move completed successfully."
        )

        # Check whether the game has ended
        self.check_game_status()

    def check_game_status(self):

        # Exit if the game is still running
        if not self.game.is_game_over():
            return

        # Prevent duplicate game-over messages
        if self.game_finished:
            return

        # Mark the game as finished
        self.game_finished = True

        # Enable saving now that the game is complete
        if not self.is_replay:
            self.save_button.config(state="normal")

        # Stop automated gameplay
        self.stop_autoplay()

        # Count remaining pegs
        remaining_pegs = sum(
            row.count(1) for row in self.game.board.cells
        )

        # Determine the player's rating
        if remaining_pegs == 1:
            rating = "Outstanding"
        elif remaining_pegs == 2:
            rating = "Very Good"
        elif remaining_pegs == 3:
            rating = "Good"
        else:
            rating = "Average"

        # Determine the result
        if self.game.is_game_won():
            result = "Congratulations! You won!"
        else:
            result = "No valid moves remain."

        # Display the final game result
        messagebox.showinfo(
            "Game Over",
            f"{result}\n\n"
            f"Pegs remaining: {remaining_pegs}\n"
            f"Your rating: {rating}"
        )

    def start_autoplay(self):

        # Clear the startup timer reference
        self.autoplay_job = None

        # Only automated games can use autoplay
        if not isinstance(self.game, AutomatedGame):
            return

        # Prevent multiple autoplay sessions
        if self.autoplay_running or self.game_finished:
            return

        # Start automated gameplay
        self.autoplay_running = True
        self.update_status("Automated game running...")

        self.autoplay_step()


    def autoplay_step(self):

        self.autoplay_job = None

        # Stop if autoplay is no longer active
        if not self.autoplay_running or self.game_finished:
            return

        # Perform the next automated move
        move_successful = self.game.autoplay_step()

        # Update the board
        self.draw_board()

        # Check whether the game has ended
        if self.game.is_game_over():
            self.autoplay_running = False
            self.check_game_status()
            return

        # Stop if no move was made
        if not move_successful:
            self.autoplay_running = False
            self.update_status("Autoplay stopped.")
            return

        # Schedule the next automated move
        self.autoplay_job = self.after(
            500,
            self.autoplay_step
        )
    
    def save_game(self):

        # Only allow saving completed games
        if not self.game_finished or self.is_replay:
            return
        
        # Ask the player where to save the recording
        filename = filedialog.asksaveasfilename(
            title="Save Game Recording",
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt")
            ]
        )

        # Player canceled the save dialog
        if not filename:
            return

        try:
            # Save the starting board and successful moves
            GameRecording.save_game(self.game, filename)

            messagebox.showinfo(
                "Game Saved",
                "Your game recording was saved successfully!"
            )

        except (OSError, ValueError, AttributeError) as error:
            messagebox.showerror(
                "Save Error",
                f"Unable to save game:\n{error}"
            )

    def start_replay(self, recorded_moves):

        # Stop automated gameplay
        self.stop_autoplay()

        # Store the recorded moves
        self.replay_moves = recorded_moves
        self.replay_index = 0

        # Enable replay mode
        self.is_replay = True
        self.replay_running = True

        # Recordings cannot be saved during replay
        self.save_button.config(state="disabled")

        # Update the status message
        self.update_status("Replaying saved game...")

        # Schedule the first recorded move
        self.replay_job = self.after(
            500,
            self.replay_step
        )
        
    def replay_step(self):

        # Clear the scheduled callback reference
        self.replay_job = None

        # Stop if replay is no longer active
        if not self.replay_running:
            return

        # Check whether all moves have been replayed
        if self.replay_index >= len(self.replay_moves):
            self.replay_running = False
            self.update_status("Replay completed.")
            return

        # Get the next recorded move
        move = self.replay_moves[self.replay_index]

        # Perform the recorded move
        move_successful = self.game.make_moves(*move)

        # Stop if the recorded move is invalid
        if not move_successful:
            self.replay_running = False
            self.update_status(
                f"Replay stopped: Invalid move {self.replay_index + 1}."
            )
            return

        # Move to the next recorded move
        self.replay_index += 1

        # Update the board and peg counter
        self.draw_board()

        # Display replay progress
        self.update_status(
            f"Replaying move {self.replay_index} "
            f"of {len(self.replay_moves)}"
        )

        # Schedule the next move
        self.replay_job = self.after(
            500,
            self.replay_step
        )

    def stop_replay(self):

        # Cancel any scheduled replay move
        if self.replay_job is not None:
            self.after_cancel(self.replay_job)
            self.replay_job = None

        self.replay_running = False

    
    
    def main_menu(self):

        # Remember whether playback was running
        was_autoplay = (
            self.autoplay_running
            or self.autoplay_job is not None
        )
        was_replaying = self.replay_running

        # Pause automated gameplay and replay
        self.stop_autoplay()
        self.stop_replay()

        # Ask before returning to setup
        confirm = messagebox.askyesno(
            "Main Menu",
            "Return to the main menu?"
        )

        if confirm:
            self.return_to_setup()

        elif was_replaying:
            # Resume replay if the player selects No
            self.replay_running = True
            self.replay_job = self.after(
                500,
                self.replay_step
            )

        elif was_autoplay:
            # Resume automated gameplay
            self.start_autoplay()


    
    def exit_game(self):

        # Remember whether playback was running
        was_autoplay = (
            self.autoplay_running
            or self.autoplay_job is not None
        )
        was_replaying = self.replay_running

        # Pause automated gameplay and replay
        self.stop_autoplay()
        self.stop_replay()

        # Ask before exiting
        confirm = messagebox.askyesno(
            "Exit Game",
            "Are you sure you want to exit?"
        )

        if confirm:
            # Close the application
            self.winfo_toplevel().destroy()

        elif was_replaying:
            # Resume replay if the player selects No
            self.replay_running = True
            self.replay_job = self.after(
                500,
                self.replay_step
            )

        elif was_autoplay:
            # Resume automated gameplay
            self.start_autoplay()


