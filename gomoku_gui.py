import tkinter as tk
from tkinter import messagebox
import copy

BOARD_SIZE = 15
CELL_SIZE = 30
EMPTY = 0
HUMAN = 1
AI = 2

# === Game Logic ===

def create_board():
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def check_five_in_a_row(board, player):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if check_direction(board, row, col, 0, 1, player) or \
               check_direction(board, row, col, 1, 0, player) or \
               check_direction(board, row, col, 1, 1, player) or \
               check_direction(board, row, col, 1, -1, player):
                return True
    return False

def check_direction(board, row, col, dx, dy, player):
    for i in range(5):
        r, c = row + i*dx, col + i*dy
        if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE) or board[r][c] != player:
            return False
    return True

def is_full(board):
    return all(cell != EMPTY for row in board for cell in row)

def get_all_valid_moves(board):
    return [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if board[r][c] == EMPTY]

def evaluate_board(board, player):
    return sum(cell == player for row in board for cell in row)

def minimax(board, depth, maximizing, player):
    opponent = HUMAN if player == AI else AI
    if check_five_in_a_row(board, player):
        return 1000, None
    if check_five_in_a_row(board, opponent):
        return -1000, None
    if depth == 0 or is_full(board):
        return evaluate_board(board, player), None

    best_move = None
    if maximizing:
        max_eval = float('-inf')
        for move in get_all_valid_moves(board):
            new_board = copy.deepcopy(board)
            new_board[move[0]][move[1]] = player
            eval_score, _ = minimax(new_board, depth - 1, False, player)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in get_all_valid_moves(board):
            new_board = copy.deepcopy(board)
            new_board[move[0]][move[1]] = opponent
            eval_score, _ = minimax(new_board, depth - 1, True, player)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
        return min_eval, best_move

def alpha_beta(board, depth, alpha, beta, maximizing, player):
    opponent = HUMAN if player == AI else AI
    if check_five_in_a_row(board, player):
        return 1000, None
    if check_five_in_a_row(board, opponent):
        return -1000, None
    if depth == 0 or is_full(board):
        return evaluate_board(board, player), None

    best_move = None
    if maximizing:
        max_eval = float('-inf')
        for move in get_all_valid_moves(board):
            new_board = copy.deepcopy(board)
            new_board[move[0]][move[1]] = player
            eval_score, _ = alpha_beta(new_board, depth - 1, alpha, beta, False, player)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in get_all_valid_moves(board):
            new_board = copy.deepcopy(board)
            new_board[move[0]][move[1]] = opponent
            eval_score, _ = alpha_beta(new_board, depth - 1, alpha, beta, True, player)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move

# === GUI ===

class GomokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gomoku - Game Solver")
        self.mode = "human"
        self.turn = HUMAN
        self.board = create_board()

        # Controls
        control_frame = tk.Frame(root)
        control_frame.pack()

        tk.Button(control_frame, text="Human vs AI", command=self.set_human_mode).pack(side=tk.LEFT)
        tk.Button(control_frame, text="AI vs AI", command=self.set_ai_vs_ai_mode).pack(side=tk.LEFT)
        tk.Button(control_frame, text="Restart", command=self.reset_game).pack(side=tk.LEFT)

        # Canvas
        self.canvas = tk.Canvas(root, width=BOARD_SIZE*CELL_SIZE, height=BOARD_SIZE*CELL_SIZE)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.human_move)
        self.draw_board()

    def set_human_mode(self):
        self.mode = "human"
        self.reset_game()

    def set_ai_vs_ai_mode(self):
        self.mode = "ai_vs_ai"
        self.reset_game()
        self.root.after(500, self.ai_vs_ai_loop)

    def reset_game(self):
        self.board = create_board()
        self.turn = HUMAN
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                x1 = j * CELL_SIZE
                y1 = i * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")
                if self.board[i][j] == HUMAN:
                    self.canvas.create_text(x1 + CELL_SIZE//2, y1 + CELL_SIZE//2, text="X", font=("Arial", 14), fill="blue")
                elif self.board[i][j] == AI:
                    self.canvas.create_text(x1 + CELL_SIZE//2, y1 + CELL_SIZE//2, text="O", font=("Arial", 14), fill="red")

    def human_move(self, event):
        if self.mode != "human":
            return

        row = event.y // CELL_SIZE
        col = event.x // CELL_SIZE
        if self.board[row][col] == EMPTY:
            self.board[row][col] = HUMAN
            self.draw_board()
            if check_five_in_a_row(self.board, HUMAN):
                messagebox.showinfo("Game Over", "🎉 You win!")
                return
            self.root.after(300, self.ai_move)

    def ai_move(self):
        _, move = minimax(self.board, depth=2, maximizing=True, player=AI)
        if move:
            self.board[move[0]][move[1]] = AI
            self.draw_board()
            if check_five_in_a_row(self.board, AI):
                messagebox.showinfo("Game Over", "🤖 AI wins!")

    def ai_vs_ai_loop(self):
        if is_full(self.board):
            messagebox.showinfo("Game Over", "🤝 It's a draw!")
            return

        if self.turn == HUMAN:
            _, move = minimax(self.board, depth=2, maximizing=True, player=HUMAN)
        else:
            _, move = alpha_beta(self.board, depth=2, alpha=float('-inf'), beta=float('inf'), maximizing=True, player=AI)

        if move:
            self.board[move[0]][move[1]] = self.turn
            self.draw_board()

            if check_five_in_a_row(self.board, self.turn):
                winner = "Minimax (X)" if self.turn == HUMAN else "Alpha-Beta (O)"
                messagebox.showinfo("Game Over", f"🏆 {winner} wins!")
                return

        self.turn = AI if self.turn == HUMAN else HUMAN
        self.root.after(400, self.ai_vs_ai_loop)

# === Main ===

if __name__ == "__main__":
    root = tk.Tk()
    app = GomokuGUI(root)
    root.mainloop()
