import tkinter as tk
import math

class BoardGraphics:

    def __init__(self, canvas):
        self.canvas = canvas
        self.cell_positions = {}

    # Board colors
        self.walnut_dark = "#382015"
        self.walnut_medium = "#583622"
        self.walnut_light = "#825536"

    # Metal colors
        self.steel_dark = "#424B55"
        self.steel_medium = "#8997A4"
        self.steel_light = "#DCE5ED"

    # Selected peg color
        self.selected_color = "#63B9FF"

    def draw_board(self, board, selected_peg=None):
        self.canvas.delete("all")
        self.cell_positions.clear()

        size = board.size

        spacing = min(68, 440 / size)

        canvas_width = int(self.canvas["width"])
        canvas_height = int(self.canvas["height"])

        board_width = (size - 1) * spacing + 110
        board_height = (size - 1) * spacing + 110

        origin_x = (canvas_width - board_width) / 2 + 55
        origin_y = (canvas_height - board_height) / 2 + 55

    # Draw wooden board
        self.draw_wood_base(origin_x, origin_y, size, spacing)

    # FIRST LOOP: Draw all playable holes
        for row in range(size):
            for col in range(size):

                if board.cells[row][col] == -1:
                    continue

                x, y = self.get_cell_position(
                    row, col, size, spacing,
                    origin_x, origin_y
                )

                self.draw_hole(x, y, spacing)

                # Store coordinates for each playable position
                self.cell_positions[(row, col)] = (x, y)

        # SECOND LOOP: Draw only occupied pegs
        for row in range(size):
            for col in range(size):

                if board.cells[row][col] != 1:
                    continue

                x, y = self.cell_positions[(row, col)]

                self.draw_peg(
                    x, y, spacing,
                    selected=(selected_peg == (row, col))
                )

    def get_cell_position(self, row, col, size, spacing, origin_x, origin_y):
    
        x = origin_x + col * spacing
        y = origin_y + row * spacing

        return x, y


    def draw_wood_base(self, origin_x, origin_y, size, spacing):
        left = origin_x - 45
        top = origin_y -45
        right = origin_x + (size-1) * spacing + 45
        bottom = origin_y + (size-1) *spacing + 45

        self.canvas.create_polygon(
            left, top + 18,
            right, top + 18,
            right, bottom + 22,
            left, bottom + 22,
            fill = self.walnut_dark,
            outline = "#21120C",
            width = 3
        )

        self.canvas.create_polygon(
            left, top,
            right, top,
            right, bottom,
            left, bottom,
            fill = self.walnut_medium,
            outline = self.walnut_light,
            width = 3
        )

        for i in range(12):
            y = top + 15 + i * (bottom - top - 30) / 12

            self.canvas.create_line(
                left + 15, y,
                right - 15, y + 4,
                fill = self.walnut_light,
                width = 1,
                smooth = True
            )

    def draw_hole(self, x, y, spacing):
        radius = spacing * 0.22

        self.canvas.create_oval(
            x - radius - 3,
            y - radius * 0.55 - 3,
            x + radius + 3,
            y + radius * 0.55 + 3,
            fill = "#956341",
            outline = "#28160F",
            width = 2
        )

        self.canvas.create_arc(
            x - radius + 3,
            y - radius * 0.55 + 2,
            x + radius - 3,
            y + radius * 0.55 - 2,
            start = 190,
            extent = 130,
            style = tk.ARC,
            outline = "#67412A",
            width = 2
        )

    def draw_peg(self, x, y, spacing, selected = False):
        head_radius = spacing * 0.19
        stem_width = spacing * 0.12
        stem_height = spacing * 0.50

        head_y = y - stem_height

        self.canvas.create_oval(
            x - head_radius,
            y - 7,
            x + head_radius,
            y + 7,
            fill = "#21140E",
            outline = ""
        )

        self.canvas.create_polygon(
            x - stem_width / 2, head_y,
            x + stem_width / 2, head_y,
            x + stem_width / 2, y,
            x - stem_width / 2, y,
            fill = self.steel_medium,
            outline = self.steel_dark,
            width = 2
        )

        self.canvas.create_rectangle(
            x + stem_width * 0.18,
            head_y + 3,
            x + stem_width / 2,
            y - 2,
            fill = self.steel_dark,
            outline=""
        )

        self.canvas.create_line(
            x - stem_width * 0.2,
            head_y + 4,
            x - stem_width * 0.2,
            y - 3,
            fill=self.steel_light,
            width=2
        )

        head_color = (
            self.selected_color if selected
            else self.steel_medium
        )

        self.canvas.create_oval(
            x - head_radius,
            head_y - head_radius * 0.65,
            x + head_radius,
            head_y + head_radius * 0.65,
            fill=head_color,
            outline=self.steel_dark,
            width=2
        )

        self.canvas.create_oval(
            x - head_radius * 0.55,
            head_y - head_radius * 0.4,
            x - head_radius * 0.05,
            head_y - head_radius * 0.12,
            fill=self.steel_light,
            outline=""
        )

        if selected:
            self.canvas.create_oval(
                x - head_radius - 5,
                head_y - head_radius * 0.65 - 5,
                x + head_radius + 5,
                head_y + head_radius * 0.65 + 5,
                outline=self.selected_color,
                width=3
            )

    
    def find_clicked_cell(self, x, y):

        for (row, col), (peg_x, peg_y) in self.cell_positions.items():

            # Detect clicks around the hole and lower stem
            hole_clicked = (
                abs(x - peg_x) <= 24
                and abs(y - peg_y) <= 24
            )

            # Detect clicks around the nail head
            # The nail head is positioned above the hole
            head_y = peg_y - 30

            head_clicked = (
                abs(x - peg_x) <= 24
                and abs(y - head_y) <= 16
            )

            if hole_clicked or head_clicked:
                return (row, col)

        return None