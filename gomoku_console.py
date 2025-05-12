import copy

# Constants
BOARD_SIZE = 15
EMPTY = 0
HUMAN = 1
AI = 2

# === Game Board Functions ===

def create_board():
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def print_board(board):
    print("\n   " + " ".join(f"{i:2}" for i in range(BOARD_SIZE)))
    for i, row in enumerate(board):
        print(f"{i:2} " + " ".join(" ." if cell == EMPTY else " X" if cell == HUMAN else " O" for cell in row))
    print()

def is_valid_move(board, row, col):
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board[row][col] == EMPTY

def make_move(board, row, col, player):
    if is_valid_move(board, row, col):
        board[row][col] = player
        return True
    return False

def is_full(board):
    return all(cell != EMPTY for row in board for cell in row)

# === Win Condition ===

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
    count = 0
    for i in range(5):
        r, c = row + i*dx, col + i*dy
        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == player:
            count += 1
        else:
            break
    return count == 5

# === AI: Minimax Algorithm ===

def get_all_valid_moves(board):
    return [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if board[r][c] == EMPTY]

def evaluate_board(board, player):
    return sum(cell == player for row in board for cell in row)

def minimax(board, depth, maximizing_player, player):
    opponent = HUMAN if player == AI else AI

    if check_five_in_a_row(board, player):
        return 1000, None
    if check_five_in_a_row(board, opponent):
        return -1000, None
    if depth == 0 or is_full(board):
        return evaluate_board(board, player), None

    best_move = None
    if maximizing_player:
        max_eval = float('-inf')
        for move in get_all_valid_moves(board):
            new_board = copy.deepcopy(board)
            make_move(new_board, move[0], move[1], player)
            eval_score, _ = minimax(new_board, depth - 1, False, player)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in get_all_valid_moves(board):
            new_board = copy.deepcopy(board)
            make_move(new_board, move[0], move[1], opponent)
            eval_score, _ = minimax(new_board, depth - 1, True, player)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
        return min_eval, best_move


def alpha_beta(board, depth, alpha, beta, maximizing_player, player):
    opponent = HUMAN if player == AI else AI

    if check_five_in_a_row(board, player):
        return 1000, None
    if check_five_in_a_row(board, opponent):
        return -1000, None
    if depth == 0 or is_full(board):
        return evaluate_board(board, player), None

    best_move = None
    if maximizing_player:
        max_eval = float('-inf')
        for move in get_all_valid_moves(board):
            new_board = copy.deepcopy(board)
            make_move(new_board, move[0], move[1], player)
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
            make_move(new_board, move[0], move[1], opponent)
            eval_score, _ = alpha_beta(new_board, depth - 1, alpha, beta, True, player)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move

# === Game Loop ===

def play_human_vs_ai():
    board = create_board()
    print_board(board)

    while True:
        # Human move
        while True:
            try:
                row = int(input("Enter row (0-14): "))
                col = int(input("Enter column (0-14): "))
                if make_move(board, row, col, HUMAN):
                    break
                print("❌ Invalid move. Try again.")
            except:
                print("❌ Please enter valid numbers.")

        print_board(board)
        if check_five_in_a_row(board, HUMAN):
            print("🎉 Human wins!")
            break
        if is_full(board):
            print("🤝 It's a draw!")
            break

        # AI move
        print("🤖 AI is thinking...")
        _, move = minimax(board, depth=2, maximizing_player=True, player=AI)
        if move:
            make_move(board, move[0], move[1], AI)
            print(f"🤖 AI played at ({move[0]}, {move[1]})")
        else:
            print("⚠️ No moves left for AI!")
        print_board(board)

        if check_five_in_a_row(board, AI):
            print("🤖 AI wins!")
            break
        if is_full(board):
            print("🤝 It's a draw!")
            break


def play_ai_vs_ai():
    board = create_board()
    print_board(board)
    turn = 0  # 0: Minimax (X), 1: Alpha-Beta (O)

    while True:
        if turn == 0:
            print("🔁 Minimax AI is thinking (Player X)...")
            _, move = minimax(board, depth=2, maximizing_player=True, player=HUMAN)
            player = HUMAN
        else:
            print("🔁 Alpha-Beta AI is thinking (Player O)...")
            _, move = alpha_beta(board, depth=2, alpha=float('-inf'), beta=float('inf'), maximizing_player=True, player=AI)
            player = AI

        if move:
            make_move(board, move[0], move[1], player)
            print(f"AI ({'X' if player == HUMAN else 'O'}) played at ({move[0]}, {move[1]})")
            print_board(board)
        else:
            print("No valid moves left!")
            break

        if check_five_in_a_row(board, player):
            print(f"🏆 AI ({'X' if player == HUMAN else 'O'}) WINS!")
            break
        if is_full(board):
            print("🤝 It's a draw!")
            break

        turn = 1 - turn  # Switch turns
        print("🔁 Switching turns...\n")

# === Main Entry ===

if __name__ == "__main__":
    print("🎮 Welcome to Gomoku (Five in a Row)")
    print("1. Play Human vs AI")
    print("2. Watch AI vs AI")
    choice = input("Choose mode (1/2): ")

    if choice == "1":
        play_human_vs_ai()
    elif choice == "2":
        play_ai_vs_ai()
    else:
        print("❌ Invalid choice.")
