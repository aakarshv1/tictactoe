#Encode tic-tac-toe generic
class Tictactoe():

    def __init__(self, rows, cols, k, misere=False, x_only=False, chaos=False, order=False):
        self.position = tuple([0]*rows*cols)
        self.rows = rows
        self.cols = cols
        self.k = k
        self.xonly = x_only
        self.misere = misere
        if misere:
            self.condition = "win"
            self.opp = "lose"
        else:
            self.condition = "lose"
            self.opp = "win"
        self.chaos = chaos
        self.order = order
        assert not (chaos and order), "chaos and order can't both go first"

    def do_move(self, position, move):
        p = list(position)[:] 
        p[move[1]] = move[0]
        return tuple(p)

    def generate_moves(self, position):
        moves = set()
        zeroes = position.count(0)
        for i, v in enumerate(position):
            if self.chaos or self.order:
                if v == 0:
                    moves.add((1, i))
                    moves.add((2, i))
            elif self.xonly:
                if v == 0:
                    moves.add((1, i))
            else:        
                if v == 0:
                    t = self.rows * self.cols
                    if (zeroes % 2 and t % 2) or not (zeroes % 2 or t % 2):
                        moves.add((1, i))
                    else:
                        moves.add((2, i))
        return moves

    def primitive_value(self, position):
        winning_combinations = self.win_combos()
        for combo in winning_combinations:
            a = position[combo[0]]
            if a == 0:
                continue
            lose = True
            for i in range(len(combo)):
                if position[combo[i]] != a:
                    lose = False
                    break
            if lose:
                if self.chaos:
                    if position.count(0) % 2:
                        return "lose"
                    else:
                        return "win"
                if self.order:
                    if position.count(0) % 2 == 0:
                        return "lose"
                    else:
                        return "win"
                return self.condition
        if position.count(0) == 0:
            if self.chaos:
                return "lose"
            if self.order:
                return "win"
            return "tie"
        else:
            return "not_primitive"

    def canonical(self, position):
        return min(self.generate_syms(position))

    def generate_syms(self, position):
        rotated_180 = self.rotate_board(position, 180)
        reflected = self.reflect_board(position)
        syms = [position, rotated_180, reflected, self.reflect_board(rotated_180)]
        if self.rows == self.cols:
            rotated_90 = self.rotate_board(position, 90)
            rotated_270 = self.rotate_board(position, 270)
            syms.extend([rotated_90, rotated_270, self.reflect_board(rotated_90), self.reflect_board(rotated_270)])
        # if self.order or self.chaos:
        #     syms.append(self.order_chaos_sym(position))
        return syms

    def order_chaos_sym(self, position):
        p = list(position)
        for i in range(len(p)):
            if p[i] == 1:
                p[i] += 1
            if p[i] == 2:
                p[i] -= 1
        return tuple(p)

    def rotate_board(self, board, degrees):
        rows = self.rows
        cols = self.cols
        rotated_board = [0] * rows * cols
        
        if degrees == 90:
            for row in range(rows):
                for col in range(cols):
                    rotated_board[col * rows + (rows - 1 - row)] = board[row * cols + col]
        elif degrees == 180:
            for row in range(rows):
                for col in range(cols):
                    rotated_board[(rows - 1 - row) * cols + (cols - 1 - col)] = board[row * cols + col]
        elif degrees == 270:
            for row in range(rows):
                for col in range(cols):
                    rotated_board[(cols - 1 - col) * rows + row] = board[row * cols + col]
        return tuple(rotated_board)
    

    def reflect_board(self, board):
        m = self.rows
        n = self.cols
        reflected_board = [0] * (m * n)
        
        for i in range(m):
            for j in range(n):
                reflected_i = i
                reflected_j = n - 1 - j  # Reflecting horizontally
                
                # Calculate the index in the reflected_board
                reflected_index = reflected_i * n + reflected_j
                
                # Copy the value from the original board to the reflected board
                reflected_board[reflected_index] = board[i * n + j]
        
        return tuple(reflected_board)

    def win_combos(self):
        r, c, k = self.rows, self.cols, self.k
    
        def horizontal_positions():
            for row in range(r):
                for col in range(c - k + 1):
                    yield [(row * c) + col + i for i in range(k)]

        def vertical_positions():
            for row in range(r - k + 1):
                for col in range(c):
                    yield [(row * c) + col + (i * c) for i in range(k)]

        def diagonal_positions():
            for row in range(r - k + 1):
                for col in range(c - k + 1):
                    yield [(row * c) + col + (i * (c + 1)) for i in range(k)]
                    yield [(row * c) + col + (k - 1) + (i * (c - 1)) for i in range(k)]

        winning_positions = list(horizontal_positions()) + list(vertical_positions()) + list(diagonal_positions())
        return winning_positions
        

if __name__ == "__main__":
    a = (1, 2, 3, 4, 5, 6, 7, 8, 9)
    t = Tictactoe(2, 2)
    print(t.canonical((2, 0, 0, 1), 2,2 ))