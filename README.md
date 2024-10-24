# tictactoe
Command Line Tic-Tac-Toe Game (m rows, n cols, k-in-a-row to win) against Perfect CPU Solver
## How to Play

1. Clone this repository to your local machine.
   ```bash
   git clone https://github.com/aakarshv1/tictactoe.git
   cd tic-tac-toe
   ```

2. Run ```python3 game.py``` in your terminal
3. You will be prompted to input the number of rows, columns, and pieces in a row required to win. You'll also be prompted to type any variants you'd like to play, the options for which are `misere`, `x_only`, `order`, and `chaos`. (Note that you can play both `misere` and `x_only` simultaneously). To play regular old tictactoe, simply press `enter`
4. After creating the game, you'll see something like this:
    ```bash
    Welcome to Tic-Tac-Toe!
      |   |  
    ---------
      |   |  
    ---------
      |   |  
    Enter your move (1-9):
    ```

Moves are represented by numbers from 1 to $mn$. Treating the tictactoe board as a matrix $A \in \mathbb{R}^{m  x  n}$, a move $k$  represents the position $A_{i,j}$ where    $i=\lceil\frac{k}{n}\rceil$ and $j=k\mod n$. 

Another way of thinking about it is that if you flatten $A$ into a vector $\vec{v} \in \mathbb{R}^{mn x 1}$ then $k$ is the entry in $\vec{v}$ that maps to the corresponding entry in $A$. 

If you didn't understand any of that don't worry I was just being annoyingly pedantic, here's the numbering for a 3x3 board. Notice how it's just counting up and wraps around after each row.

    1 | 2 | 3  
    ---------
    4 | 5 | 6 
    ---------
    7 | 8 | 9 
    
5. The CPU will play automatically and you guys can go back and forth until the game ends. I recommend trying out different board sizes and k values (number in a row required to win). It can make an otherwise very simple game a lot more interesting! Note that boards 4x4 and larger take a lot longer to load, because of computational complexity (see [How it Works](#how-it-horks) for more info).

## How it Works

If you migrate over to the file `solver.py` you can see the magic behind the scenes of the perfect CPU opponent. The idea is actually very simple: the solver recurses through the game tree through **DFS (Depth-First-Search)** and basically determines all possible outcomes of the tictactoe game (yeah sorry, if you thought you were being unique the computer had already seen your move). As you may imagine, there are a lot of outcomes to a tictactoe game so solving at each step must take a while and be quite intensive. Fortunately, we can utilize a few simple tricks. 

1. The first and probably most important one is **memoization**. This is the idea of storing game states in a cache (hashmap to be specific), so when the solver gets to a state its already seen it can simply pull the result from the cache instead of recalculating it. The other advantage of the cache is that the board basically only needs to be completely solved once (this is what happens when the board is "loading"). After that, all the possible positions have been stored by the CPU. 
2. The other main trick we use is symmetry. Essentially, we can take advantage of geometric symmetries in a tictactoe board and realize that some outcomes are just the the same but rotated or reflected, so the possible outcomes are the same (A normal 3x3 game of tictactoe has almost 11,000 possible positions, but with symmetries we can get that number down to 765 positions). 

You may be wondering, okay great, the CPU can see what all the positions are, how does it know which moves to take? The answer is ChatGP-just kidding, sorry to burst your bubble but there's no large language models here, just simple combinatorial game theory. The answer lies in what's actually being stored in the cache. 

There are two values: the primitive state (win, loss, or tie) and the remoteness. The primitive state determines what result lies at the end of the path if that move is taken, and the remoteness determines how long that path is. Therefore, given a series of available of moves, the CPU will prioritize a win with the lowest remoteness value so it takes the dub and does so as quickly as possible. If there are no wins, it looks for ties, and if no ties, it tries to prolongue its suffeirng by chossing the loss with the highest remoteness.

I encourage you to checkout `solver.py` and play around with the `remoteness_analysis` function that tells you you many winning, losing, and tieing positions there are for each possible remoteness value.

## Next Steps

Here are some improvements I'm working on:
- 2 player mode so you can play with your friends!
- 'AI' Copilot which is an optional mode where the CPU tells you what the optimal move is
- GUI to make the game a little more aesthetically pleasing and easy to interact with
- Numerical hashing (minimize sparcity)
- More efficient solving (Parallel, GPU, Cython???)

## Credits
Thank you to Prof. Dan Garcia @ UC Berkeley and the [Gamescrafters](http://gamescrafters.berkeley.edu/) group for the inspiration This was actually part of a project as a member of the group, but I wanted to share it here because I thought it was super cool. For the record, I wrote all the code by myself (may or may not have also hired an software developer consultant from OpenAI :)) but the ideas come from what discussed in the game theory research group. The code is by no means perfect, so please feel free to reach out with any bugs, recommendations, or questions!

