from tictactoe_variants import Tictactoe

cache = {}

def solve(game, sym=False, position="none"):
    if position == "none":
        position = game.position
    if sym == True:
        position = game.canonical(position)
    if position in cache:
        return cache[position]
    else:
        primval = game.primitive_value(position)
        if primval != "not_primitive":
            cache[position] = (primval, 0)
            return (primval, 0)
        else:
            moves = game.generate_moves(position)
            res = [solve(game, sym, game.do_move(position, m)) for m in moves]
            if any([x[0] == "lose" for x in res]):
                losing_children = [x for x in res if x[0] == "lose"]
                ans = ("win", min(losing_children, key=lambda x:x[1])[1] + 1)
                cache[position] = ans
                return ans
            elif res and all([x[0] == "win" for x in res]):
                ans = ("lose", max(res, key=lambda x:x[1])[1] + 1)
                cache[position] = ans
                return ans
            else:
                tying_children = [x for x in res if x[0] == "tie"]
                ans = ("tie", min(tying_children, key=lambda x:x[0])[1] + 1)
                cache[position] = ans
                return ans

def print_board(board, rows, cols):
    for i in range(rows):
        row_str = " | ".join(board[i * cols:i * cols + cols])
        print(row_str)
        if i < rows - 1:
            print("-" * (len(row_str)))

def player_move(board, rows, cols):
    slots = rows * cols
    while True:
        try:
            move = int(input(f"Enter your move (1-{slots}): "))
            if 1 <= move <= slots and board[move - 1] == " ":
                return move - 1
            else:
                print("Invalid move. Please try again.")
        except ValueError:
            print(f"Invalid input. Please enter a number between 1 and {slots}.")

def cpu_move(game, position):
    moves = game.generate_moves(position)
    best_win_remoteness = float('inf')
    best_move = None

    for move in moves:
        new_position = game.canonical(game.do_move(position, move))
        result, remoteness = cache[new_position]

        if result == "lose" and remoteness < best_win_remoteness:
            best_win_remoteness = remoteness
            best_move = move
    
    if not best_move:
        for move in moves:
            new_position = game.canonical(game.do_move(position, move))
            result, remoteness = cache[new_position]

            if result == "tie" and remoteness < best_win_remoteness:
                best_win_remoteness = remoteness
                best_move = move

    if not best_move:
        best_win_remoteness = 0
        for move in moves:
            new_position = game.canonical(game.do_move(position, move))
            result, remoteness = cache[new_position]

            if remoteness > best_win_remoteness:
                best_win_remoteness = remoteness
                best_move = move


    # Convert the tuple move to an integer index
    move_index = best_move[1]

    return move_index


def play_tic_tac_toe(rows, cols, k, misere, x_only, chaos, order):
    tictactoe_game = Tictactoe(rows, cols, k, misere=misere, x_only=x_only, chaos=chaos, order=order)
    solve(tictactoe_game, sym=True)
    board = [" " for _ in range(rows*cols)]
    player_turn = True

    print("Welcome to Tic-Tac-Toe!")
    print_board(board, rows, cols)

    while True:
        if player_turn:
            move = player_move(board, rows, cols)
        else:
            m = tuple(map(lambda x: 2 if x == 'O' else (1 if x == 'X' else 0), board))
            move = cpu_move(tictactoe_game, m)

        if player_turn:
            board[move] = 'X'
        else:
            board[move] = 'O'

        print_board(board, rows, cols)
        print('-' * 20)
        m = tuple(map(lambda x: 1 if x == 'X' else (2 if x == 'O' else 0), board))
        result = tictactoe_game.primitive_value(m)

        if result == "win":
            if player_turn:
                print("CPU wins! Better luck next time.")
            else:
                print("Congratulations! You win!")
            break
        elif result == "lose":
            if player_turn:
                print("Congratulations! You win!")
            else:
                print("CPU wins! Better luck next time.")
            break
        elif result == "tie":
            print("It's a tie!")
            break

        player_turn = not player_turn

if __name__ == "__main__":
    rows = int(input("How many rows?\n"))
    cols = int(input("How many cols?\n"))
    k = int(input("How many in a row to win?\n"))
    var = input("Any variants?\n")
    misere, x_only, chaos, order = False, False, False, False
    if "misere" in var:
        misere = True
    if "x_only" in var:
        x_only = True
    if "chaos" in var:
        chaos = True
    if "order" in var:
        order = True
    play_tic_tac_toe(rows, cols, k, misere, x_only, chaos, order)
