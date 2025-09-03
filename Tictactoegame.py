import tkinter

def game_board(row, column):
    global currentPlayer
    if game_over or board[row][column]["text"] != "":
        return

    board[row][column]["text"] = currentPlayer
    results()

    if not game_over:
        currentPlayer = playerO
        label["text"] = currentPlayer + "'s turn"
        row_bob, col_bob = best_move()
        board[row_bob][col_bob]["text"] = currentPlayer
        results()
        currentPlayer = playerX
        label["text"] = currentPlayer + "'s turn"

def update_score(winner):
    global scoreX, scoreO
    if winner == "X":
        scoreX += 1
    elif winner == "O":
        scoreO += 1
    score_label.config(text=f"Score - X: {scoreX} | O: {scoreO}")

def new_game():
    global turns, game_over, currentPlayer
    turns = 0
    game_over = False
    currentPlayer = playerX
    label.config(text=currentPlayer + "'s turn", foreground="white")
    for row in range (3):
        for column in range (3):
            board[row][column].config(text="", foreground=blue, background=gray)

def results():
    global turns, game_over, scoreX, scoreO
    turns += 1

    for row in range(3):
        if board[row][0]["text"] == board[row][1]["text"] == board[row][2]["text"] and board[row][0]["text"] != "":
            winner = board[row][0]["text"]
            label.config(text=winner + " is the winner!", foreground=yellow)
            for column in range(3):
                board[row][column].config(foreground=yellow, background=lightGray)
            game_over = True
            update_score(winner)
            return

    for column in range(3):
        if board[0][column]["text"] == board[1][column]["text"] == board[2][column]["text"] and board[0][column]["text"] != "":
            winner = board[0][column]["text"]
            label.config(text=winner + " is the winner!", foreground=yellow)
            for row in range(3):
                board[row][column].config(foreground=yellow, background=lightGray)
            game_over = True
            update_score(winner)
            return

    if board[0][0]["text"] == board[1][1]["text"] == board[2][2]["text"] and board[0][0]["text"] != "":
        winner = board[0][0]["text"]
        label.config(text=winner + " is the winner!", foreground=yellow)
        for i in range(3):
            board[i][i].config(foreground=yellow, background=lightGray)
        game_over = True
        update_score(winner)
        return

    if board[0][2]["text"] == board[1][1]["text"] == board[2][0]["text"] and board[0][2]["text"] != "":
        winner = board[0][2]["text"]
        label.config(text=winner + " is the winner!", foreground=yellow)
        board[0][2].config(foreground=yellow, background=lightGray)
        board[1][1].config(foreground=yellow, background=lightGray)
        board[2][0].config(foreground=yellow, background=lightGray)
        game_over = True
        update_score(winner)
        return

    if turns == 9:
        game_over = True
        label.config(text="Tie!", foreground=yellow)

def best_move():
    best_score = -float('inf')
    move = None
    for row in range(3):
        for col in range(3):
            if board[row][col]["text"] == "":
                board[row][col]["text"] = playerO
                score = minimax(False)
                board[row][col]["text"] = ""
                if score > best_score:
                    best_score = score
                    move = (row, col)
    return move

def get_empty_cells():
    return [(row, col) for row in range(3) for col in range(3) if board[row][col]["text"] == ""]

def minimax(is_maximizing):
    result = check_winner()
    if result == playerO:
        return 1
    elif result == playerX:
        return -1
    elif is_full():
        return 0

    best_score = -float('inf') if is_maximizing else float('inf')

    for row, col in get_empty_cells():
        board[row][col]["text"] = playerO if is_maximizing else playerX
        score = minimax(not is_maximizing)
        board[row][col]["text"] = ""

        if is_maximizing:
            best_score = max(score, best_score)
        else:
            best_score = min(score, best_score)

    return best_score

def is_full():
    return all(board[row][col]["text"] != "" for row in range(3) for col in range(3))

def check_winner():
    for row in range(3):
        if board[row][0]["text"] == board[row][1]["text"] == board[row][2]["text"] != "":
            return board[row][0]["text"]
    for col in range(3):
        if board[0][col]["text"] == board[1][col]["text"] == board[2][col]["text"] != "":
            return board[0][col]["text"]
    if board[0][0]["text"] == board[1][1]["text"] == board[2][2]["text"] != "":
        return board[0][0]["text"]
    if board[0][2]["text"] == board[1][1]["text"] == board[2][0]["text"] != "":
        return board[0][2]["text"]
    return None

playerX = "X"
playerO = "O"
currentPlayer = playerX
board = [
    [0,0,0],
    [0,0,0],
    [0,0,0]
]

blue = "#4584b6"
yellow = "#ffde57"
gray = "#343434"
lightGray = "#646464"

turns = 0
game_over = False
scoreX = 0
scoreO = 0
time_left = 60

window = tkinter.Tk()
window.title("Tic Tac Toe")
window.resizable(True, True)


frame = tkinter.Frame(window)
label = tkinter.Label(frame, text = currentPlayer + "'s turn", font = ("Consolas", 20), background = gray, foreground = "white")
label.grid(row = 0, column = 0, columnspan = 3, sticky = "we")

for row in range(3):
    for column in range(3):
        board[row][column] = tkinter.Button(frame, text = "", font = ("Consolas", 50, "bold"), background=gray, foreground=blue, width=4, height=1, command=lambda row=row, column=column: game_board(row,column))
        board[row][column].grid(row=row + 1, column=column)

button = tkinter.Button(frame, text="restart", font=("Consolas", 20), background=gray, foreground="white", command=new_game)
button.grid(row=4, column=0, columnspan=3, sticky="we")

score_label = tkinter.Label(frame, text=f"Score - X: {scoreX} | O: {scoreO}", font=("Consolas", 15),background=gray, foreground="white")
score_label.grid(row=5, column=0, columnspan=3, sticky="we")

timer_label = tkinter.Label(frame, text=f"Time left: {time_left}s", font=("Consolas", 15), background=gray, foreground="white")
timer_label.grid(row=6, column=0, columnspan=3, sticky="we")

frame.pack()

window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

def start_timer():
    global time_left, game_over
    if time_left > 0:
        timer_label.config(text=f"Time left: {time_left}s")
        time_left -= 1
        window.after(1000, start_timer)
    else:
        game_over = True
        label.config(text=f"Time's up! Final Score - X: {scoreX} | O: {scoreO}", foreground=yellow)

start_timer()

window.mainloop()
