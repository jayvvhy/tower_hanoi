# tower_hanoi
Recursive solution to Tower of Hanoi problem with log n complexity

This was my solution to one of the assignments during my Master Programme. The Tower of Hanoi game is a common problem used to teach recursion in computing courses but the problem given was a slight variation.

The general rules of the tower of hanoi game is as follow:
1. All disks start on one peg and the objective is to move all disks from one peg to the other.
2. Only one (the top) disk on any peg may be moved each time.
3. Larger disks cannot be stacked over smaller ones.

Additional rule imposed in my problem:
The smallest disk (disk 1) will always have to move in a clockwise fashion from peg A to peg B to peg C before looping back to peg A.
Solution needs to accommodate 'edge' cases with a maximum of 64 disks in play.
Solution needs to complete within 30ms.

Further context of problem:
The function needs to achieve two things:
1. Given a mid-game state of the disks and their current peg location, determine what was the origin peg - existing state could also be an impossible state to reach regardless of which peg was the origin.
2. Should the given state not be an impossible one, also identify the state it will be in X moves later (X being a large integer number given with the state)

Many of the tower of hanoi solutions online employ a simple recursion defining a source (origin) / target (destination) / auxiliary (spare) peg to 'solve' the movement of disks from one peg to another. However, this problem required identifying the origin rod given a mid-game state of the disks.

There are a few conundrums in this problem:
1. While it is obvious what the first move the recursion should make if all pegs are on the same starting peg, this is ambiguous in a mid-game state and there may exist more than one legal next move.
2. As n (number of disks) could be large - 64 disks would imply 2^64-1 = 18,446,744,073,709,551,615 moves to be made from start to end, the base case recursion would not be able to feasibly complete the recursion due to memory and time limitations.

Solution in brief:
As disk 1 will be moved on every other move, the solution employed first attempts calling the recursion function (state_step) with the assumption that the next valid move is moving disk 1. If recursion reaches an end state where all disks are on a single peg, state_step is then called again with a specified moves (mm) parameter which will advance the state by mm number of moves to arrive at the state required by the problem. Should the first recursion call fail to yield an end state, state_step is called again  this time with the assumption that the next valid move is moving the next smallest disk other than disk 1. Impossible would be printed in the output if this call does not resolve the end state. In the event that an end state is reached on the second call, state_step is invoked for the last time wit a specified mm parameter which will advance the state by mm moves.

To drastically reduce the number of recursive calls, the state_step function identifies running stacks (i.e. (1,2) / (1,2,3) / (1,2,3,...,n)) of pegs on moves where it is legal to move disk 1 and fast forwards the recursion by moving the entire stack at once while decrementing the move limit (mm). This trivializes the complexity of the recursion to O(log n) as the stack height increases exponentially with every other move until end state is reached. Originally an additional condition was present which required the stack to be placed on top of the next larger disk (i.e. stack containg 1,2,3 will only be moved as a stack if there was an exposed disk 4 in the valid direction of movement) - this was with the intention to 'connect' the stacks to accelerate the recursion but this caused an issue when an mm parameter was specified and the remaining number of moves specified was insufficient to move the identified stack. Removal of said condition and addition of a new condition which constrained the stack height based on the remaining number of moves resolved the issue.

This was an interesting problem to work on in optimizing a recursion algorithm with strict constraints on time complexities.
