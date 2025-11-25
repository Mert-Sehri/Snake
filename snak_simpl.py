import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")

        # --- Game settings ---
        self.WIDTH = 600
        self.HEIGHT = 600
        self.CELL_SIZE = 20
        self.COLS = self.WIDTH // self.CELL_SIZE
        self.ROWS = self.HEIGHT // self.CELL_SIZE
        self.SPEED = 100  # milliseconds per move

        # Colors
        self.BG_COLOR = "#1e1e1e"
        self.SNAKE_COLOR = "#4caf50"
        self.SNAKE_HEAD_COLOR = "#81c784"
        self.FOOD_COLOR = "#ff5722"
        self.GRID_COLOR = "#2c2c2c"
        self.TEXT_COLOR = "#ffffff"

        # Game state variables
        self.direction = "Right"
        self.next_direction = "Right"
        self.snake = []
        self.food = None
        self.score = 0
        self.game_running = False

        # --- UI setup ---
        self.setup_ui()
        self.reset_game()

    def setup_ui(self):
        # Score label
        self.score_var = tk.StringVar()
        self.score_var.set("Score: 0")

        score_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        score_frame.pack(fill="x")

        score_label = tk.Label(
            score_frame,
            textvariable=self.score_var,
            font=("Consolas", 16),
            fg=self.TEXT_COLOR,
            bg=self.BG_COLOR,
            pady=5
        )
        score_label.pack(side="left", padx=10)

        info_label = tk.Label(
            score_frame,
            text="Use arrow keys or WASD • Press R to restart",
            font=("Consolas", 10),
            fg="#bbbbbb",
            bg=self.BG_COLOR
        )
        info_label.pack(side="right", padx=10)

        # Canvas
        self.canvas = tk.Canvas(
            self.root,
            width=self.WIDTH,
            height=self.HEIGHT,
            bg=self.BG_COLOR,
            highlightthickness=0
        )
        self.canvas.pack()

        # Draw grid (optional visual)
        for x in range(0, self.WIDTH, self.CELL_SIZE):
            self.canvas.create_line(x, 0, x, self.HEIGHT, fill=self.GRID_COLOR)
        for y in range(0, self.HEIGHT, self.CELL_SIZE):
            self.canvas.create_line(0, y, self.WIDTH, y, fill=self.GRID_COLOR)

        # Bind keys
        self.root.bind("<Up>", self.on_key_press)
        self.root.bind("<Down>", self.on_key_press)
        self.root.bind("<Left>", self.on_key_press)
        self.root.bind("<Right>", self.on_key_press)
        self.root.bind("<w>", self.on_key_press)
        self.root.bind("<a>", self.on_key_press)
        self.root.bind("<s>", self.on_key_press)
        self.root.bind("<d>", self.on_key_press)
        self.root.bind("<W>", self.on_key_press)
        self.root.bind("<A>", self.on_key_press)
        self.root.bind("<S>", self.on_key_press)
        self.root.bind("<D>", self.on_key_press)
        self.root.bind("<r>", self.on_restart)
        self.root.bind("<R>", self.on_restart)
        self.root.bind("<space>", self.on_restart)

    def reset_game(self):
        # Initial snake in center, length 3
        start_x = self.COLS // 2
        start_y = self.ROWS // 2
        self.snake = [
            (start_x - 1, start_y),
            (start_x, start_y),
            (start_x + 1, start_y),
        ]
        self.direction = "Right"
        self.next_direction = "Right"
        self.score = 0
        self.score_var.set(f"Score: {self.score}")
        self.game_running = True

        # Clear canvas objects but leave grid (tag trick)
        self.canvas.delete("snake")
        self.canvas.delete("food")
        self.canvas.delete("overlay")

        self.spawn_food()
        self.draw_snake()
        self.draw_food()
        self.game_loop()

    def on_restart(self, event=None):
        if not self.game_running:
            self.reset_game()

    def on_key_press(self, event):
        key = event.keysym

        if key in ["Up", "w", "W"]:
            if self.direction != "Down":  # prevent reverse
                self.next_direction = "Up"
        elif key in ["Down", "s", "S"]:
            if self.direction != "Up":
                self.next_direction = "Down"
        elif key in ["Left", "a", "A"]:
            if self.direction != "Right":
                self.next_direction = "Left"
        elif key in ["Right", "d", "D"]:
            if self.direction != "Left":
                self.next_direction = "Right"

    def game_loop(self):
        if not self.game_running:
            return

        self.direction = self.next_direction
        self.move_snake()
        self.root.after(self.SPEED, self.game_loop)

    def move_snake(self):
        head_x, head_y = self.snake[-1]

        if self.direction == "Up":
            new_head = (head_x, head_y - 1)
        elif self.direction == "Down":
            new_head = (head_x, head_y + 1)
        elif self.direction == "Left":
            new_head = (head_x - 1, head_y)
        else:  # Right
            new_head = (head_x + 1, head_y)

        new_x, new_y = new_head

        # Check wall collision
        if not (0 <= new_x < self.COLS and 0 <= new_y < self.ROWS):
            self.game_over()
            return

        # Check self collision
        if new_head in self.snake:
            self.game_over()
            return

        # Move snake
        self.snake.append(new_head)

        # Check food collision
        if new_head == self.food:
            self.score += 1
            self.score_var.set(f"Score: {self.score}")
            self.spawn_food()
        else:
            # Remove tail (no growth)
            self.snake.pop(0)

        # Redraw
        self.canvas.delete("snake")
        self.canvas.delete("food")
        self.draw_snake()
        self.draw_food()

    def draw_snake(self):
        for i, (x, y) in enumerate(self.snake):
            x1 = x * self.CELL_SIZE
            y1 = y * self.CELL_SIZE
            x2 = x1 + self.CELL_SIZE
            y2 = y1 + self.CELL_SIZE

            # Head slightly different color
            color = self.SNAKE_HEAD_COLOR if i == len(self.snake) - 1 else self.SNAKE_COLOR
            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=color,
                outline="#000000",
                tags="snake"
            )

    def draw_food(self):
        if self.food is None:
            return
        x, y = self.food
        x1 = x * self.CELL_SIZE + 2
        y1 = y * self.CELL_SIZE + 2
        x2 = x1 + self.CELL_SIZE - 4
        y2 = y1 + self.CELL_SIZE - 4
        self.canvas.create_oval(
            x1, y1, x2, y2,
            fill=self.FOOD_COLOR,
            outline="",
            tags="food"
        )

    def spawn_food(self):
        # Random position not on snake
        while True:
            x = random.randint(0, self.COLS - 1)
            y = random.randint(0, self.ROWS - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def game_over(self):
        self.game_running = False

        # Dark overlay
        self.canvas.create_rectangle(
            0, 0, self.WIDTH, self.HEIGHT,
            fill="#000000",
            stipple="gray50",
            outline="",
            tags="overlay"
        )

        # Game over text
        self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2 - 20,
            text="GAME OVER",
            fill=self.TEXT_COLOR,
            font=("Consolas", 32, "bold"),
            tags="overlay"
        )

        self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2 + 20,
            text=f"Final Score: {self.score}",
            fill="#dddddd",
            font=("Consolas", 18),
            tags="overlay"
        )

        self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2 + 60,
            text="Press R or Space to restart",
            fill="#aaaaaa",
            font=("Consolas", 12),
            tags="overlay"
        )


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
