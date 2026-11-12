import tkinter as tk
import random

from tkinter import filedialog, messagebox
from Recording import GameRecording

class SetupScreen(tk.Frame):

    def __init__(self, parent, on_start, on_replay):
        super().__init__(parent, bg="#171B22")

        # Callback used to start the game
        self.on_start = on_start

        # Callback used to replay a saved game
        self.on_replay = on_replay

        # Default selections
        self.game_mode = tk.StringVar(value="Manual")
        self.board_type = tk.StringVar(value="English")
        self.board_size = tk.IntVar(value=7)

        # Track whether the board should be randomized
        self.randomize_board = False
        

        # Build the setup interface
        self.create_widgets()

    def create_choice_card(self, parent, text, variable, value):
        card = tk.Label(
            parent,
            text=text,
            font=("Arial", 13, "bold"),
            bg="#292D34",
            fg="white",
            width=18,
            height=2,
            cursor="hand2",
            relief="solid",
            bd=2
        )

        card.pack(pady=6, padx=8)

        
        def select_card(event=None):

            # Update the selected card
            variable.set(value)

            # Manually changing board shape or size
            # cancels randomization
            if variable is self.board_type or variable is self.board_size:
                self.randomize_board = False
                self.randomize_appearance()


        card.bind("<Button-1>", select_card)

        def update_appearance(*args):
            if variable.get() == value:
                card.config(
                    bg="#825536",
                    highlightbackground="#E8BA87",
                    highlightthickness=2
                )
            else:
                card.config(
                    bg="#292D34",
                    highlightthickness=0
                )

        variable.trace_add("write", update_appearance)
        update_appearance()

        return card

    
    def create_widgets(self):

        # Main title
        tk.Label(
            self,
            text="PEG SOLITAIRE",
            font=("Arial", 26, "bold"),
            bg="#171B22",
            fg="#E6E6E6"
        ).pack(pady=(25, 10))

        tk.Label(
            self,
            text="Choose your game settings",
            font=("Arial", 13),
            bg="#171B22",
            fg="#AAB5C0"
        ).pack(pady=(0, 30))

        # Top section: two columns
        top_frame = tk.Frame(self, bg="#171B22")
        top_frame.pack(pady=10)

        # LEFT: game mode
        mode_frame = tk.Frame(
            top_frame,
            bg="#171B22",
            width=350
        )
        mode_frame.grid(row=0, column=0, padx=35, sticky="n")

        tk.Label(
            mode_frame,
            text="How would you like to play?",
            font=("Arial", 14, "bold"),
            bg="#171B22",
            fg="white"
        ).pack(pady=(0, 20))

        for mode in ["Manual", "Automated"]:
            self.create_choice_card(
                mode_frame,
                f"{mode} Play",
                self.game_mode,
                mode
            )

        # RIGHT: board shape
        shape_frame = tk.Frame(
            top_frame,
            bg="#171B22",
            width=350
        )
        shape_frame.grid(row=0, column=1, padx=35, sticky="n")

        tk.Label(
            shape_frame,
            text="Choose your board shape",
            font=("Arial", 14, "bold"),
            bg="#171B22",
            fg="white"
        ).pack(pady=(0, 20))

        for shape in ["English", "Diamond", "Hexagon"]:
            self.create_choice_card(
                shape_frame,
                shape,
                self.board_type,
                shape
            )

        # BOTTOM: board size
        size_frame = tk.Frame(self, bg="#171B22")
        size_frame.pack(pady=(30, 15))

        tk.Label(
            size_frame,
            text="Choose your board size",
            font=("Arial", 14, "bold"),
            bg="#171B22",
            fg="white"
        ).pack(pady=(0, 15))

        size_cards = tk.Frame(size_frame, bg="#171B22")
        size_cards.pack()

        for size in [5, 7, 9]:

            card_container = tk.Frame(
                size_cards,
                bg="#171B22"
            )
            card_container.pack(side="left", padx=12)

            self.create_choice_card(
                card_container,
                f"{size} x {size}",
                self.board_size,
                size
            )     
        
        # RANDOMIZE BOARD SECTION
        random_frame = tk.Frame(
            self,
            bg="#171B22"
        )
        random_frame.pack(pady=(15, 5))

        tk.Label(
            random_frame,
            text="Or let the game choose for you",
            font=("Arial", 13),
            bg="#171B22",
            fg="#AAB5C0"
        ).pack(pady=(0, 10))

        # Randomize Board button
        self.randomize_button = tk.Button(
            random_frame,
            text="RANDOMIZE",
            font=("Arial", 12, "bold"),
            bg="#292D34",
            fg="white",
            activebackground="#A56B42",
            activeforeground="white",
            padx=25,
            pady=10,
            cursor="hand2",
            command=self.randomize_settings
        )
        self.randomize_button.pack()

        # START GAME
        tk.Button(
            self,
            text="START GAME",
            font=("Arial", 14, "bold"),
            bg="#825536",
            fg="white",
            activebackground="#A56B42",
            activeforeground="white",
            padx=35,
            pady=12,
            cursor="hand2",
            command=self.start_game
        ).pack(pady=25)

    
        # REPLAY GAME button
        tk.Button(
            self,
            text="REPLAY GAME",
            font=("Arial", 12, "bold"),
            bg="#292D34",
            fg="white",
            activebackground="#2563EB",
            activeforeground="white",
            padx=25,
            pady=10,
            cursor="hand2",
            command=self.replay_game
        ).pack(pady=(0, 15))

    def randomize_appearance(self):
        if self.randomize_board:
            # Blue when randomization is selected
            self.randomize_button.config(
                bg="#2563EB"
            )
        else:
            # Dark gray when randomization is deselected
            self.randomize_button.config(
                bg="#292D34"
            )

    
    def randomize_settings(self):

        # Clicking again turns randomization off
        if self.randomize_board:
            self.randomize_board = False
            self.randomize_appearance()
            return

        # Get the current board settings
        current_shape = self.board_type.get()
        current_size = self.board_size.get()

        # Generate every possible board combination
        combinations = [
            (shape, size)
            for shape in ["English", "Diamond", "Hexagon"]
            for size in [5, 7, 9]
        ]

        # Exclude the currently selected combination
        combinations.remove((current_shape, current_size))

        # Randomly select a different combination
        shape, size = random.choice(combinations)

        # Update the selected board settings
        self.board_type.set(shape)
        self.board_size.set(size)

        # Enable random starting hole
        self.randomize_board = True

        # Update the RANDOMIZE button appearance
        self.randomize_appearance()


    def start_game(self):

        # Get the player's selections
        mode = self.game_mode.get()
        board_type = self.board_type.get()
        size = self.board_size.get()

        # Send selections and randomization choice
        # to the GUI controller
        self.on_start(
            mode,
            board_type,
            size,
            self.randomize_board
        )


    def replay_game(self):

        # Ask the player to choose a saved recording
        filename = filedialog.askopenfilename(
            title="Select Game Recording",
            filetypes=[
                ("Text Files", "*.txt")
            ]
        )

        # Player canceled the file dialog
        if not filename:
            return

        try:
            # Load the recording data
            game_data = GameRecording.load_game(filename)

            # Pass the recording to the GUI controller
            self.on_replay(game_data)

        except (OSError, ValueError, KeyError) as error:
            messagebox.showerror(
                "Replay Error",
                f"Unable to load recording:\n{error}"
            )
