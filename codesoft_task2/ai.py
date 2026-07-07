WINNING_COMBINATIONS = [
    [0,1,2], [3,4,5], [6,7,8],
    [0,3,6], [1,4,7], [2,5,8],
    [0,4,8], [2,4,6]
]

def check_winner(board):
    for combo in WINNING_COMBINATIONS:
        a, b, c = combo

        if board[a] == board[b] == board[c] != "":
            return board[a]

    if "" not in board:
        return "Draw"

    return None


def minimax(board, is_maximizing):
    result = check_winner(board)

    if result == "O":
        return 1

    if result == "X":
        return -1

    if result == "Draw":
        return 0

    if is_maximizing:
        best_score = -100

        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax(board, False)
                board[i] = ""
                best_score = max(score, best_score)

        return best_score

    else:
        best_score = 100

        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                score = minimax(board, True)
                board[i] = ""
                best_score = min(score, best_score)

        return best_score


def best_move(board):
    best_score = -100
    move = None

    for i in range(9):
        if board[i] == "":
            board[i] = "O"

            score = minimax(board, False)

            board[i] = ""

            if score > best_score:
                best_score = score
                move = i

    return move