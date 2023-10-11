from homefun5.tictactoe_variants import Tictactoe
import time

## General solver for game encodings

cache = {}

def solve(game, sym=False, position="none"):
    # height = game.rows
    # width = game.cols
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

def remoteness_analysis(cache):
    outcomes = ["win", "lose", "tie"]
    remote = {}
    for v in cache.values():
        r, o = v[1], v[0]
        if r not in remote:
            remote[r] = [0, 0, 0]
        remote[r][outcomes.index(o)] += 1
    totalw, totall, totalt, total = position_analysis(cache)
    print(f"{'Remote':<10}{'Win':<10}{'Lose':<10}{'Tie':<10}{'Total':<10}")
    print("-" * 40)
    sorted_keys = list(remote.keys())
    sorted_keys.sort(reverse=True)
    for k in sorted_keys:

        print(f"{k:<10}{remote[k][0]:<10}{remote[k][1]:<10}{remote[k][2]:<10}{sum(remote[k]):<10}")
    print("-" * 40)
    print(f"{'Total':<10}{totalw:<10}{totall:<10}{totalt:<10}{total:<10}")

def position_analysis(cache):
    wins = 0
    prim_losses = 0
    prim_ties = 0
    total_losses = 0
    total_ties = 0

    for i in cache.values():
        if i[0] == "win":
            wins += 1
        if i[0] == "lose":
            total_losses += 1
            if i[1] == 0:
                prim_losses += 1
        if i[0] == "tie":
            total_ties += 1
            if i[1] == 0:
                prim_ties += 1
    total = wins + total_ties + total_losses
    return (wins, total_losses, total_ties, total)

if __name__ == "__main__":
    h = 2
    w = 2
    k = 2
    start = time.time()
    solve(Tictactoe(h, w, k, misere=True), sym=True)
    end = time.time()
    print(f"\n\nTic-Tac-Toe ({h}x{w}) Original (without symmetries)\n")
    print("Time Elapsed: ", end-start)
    remoteness_analysis(cache)
    # cache = {}
    # start = time.time()
    # solve(Tictactoe(h, w, misere=True), sym=True)
    # end = time.time()
    # print(f"\n\nTic-Tac-Toe ({h}x{w}) Misere (without symmetries)\n")
    # print("Time Elapsed: ", end-start)
    # remoteness_analysis(cache)
    # cache = {}
    # start = time.time()
    # solve(Tictactoe(h, w, x_only=True), sym=True)
    # end = time.time()
    # print(f"\n\nTic-Tac-Toe ({h}x{w}) X-Only (without symmetries)\n")
    # print("Time Elapsed: ", end-start)
    # remoteness_analysis(cache)
    # cache = {}
    # start = time.time()
    # solve(Tictactoe(h, w, misere=True, x_only=True), sym=True)
    # end = time.time()
    # print(f"\n\nTic-Tac-Toe ({h}x{w}) Misere and X-Only (without symmetries)\n")
    # print("Time Elapsed: ", end-start)
    # remoteness_analysis(cache)
    # cache = {}
    # start = time.time()
    # solve(Tictactoe(h, w, order=True), sym=True)
    # end = time.time()
    # print(f"\n\nTic-Tac-Toe ({h}x{w}) Order First (without symmetries)\n")
    # print("Time Elapsed: ", end-start)
    # remoteness_analysis(cache)
    # cache = {}
    # start = time.time()
    # solve(Tictactoe(h, w, chaos=True), sym=True)
    # end = time.time()
    # print(f"\n\nTic-Tac-Toe ({h}x{w}) Chaos First (without symmetries)\n")
    # print("Time Elapsed: ", end-start)
    # remoteness_analysis(cache)
    