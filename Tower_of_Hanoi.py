import copy
import sys
#sys.setrecursionlimit(10**6)  # Set a higher limit

def state_to_str(state):
    s = [' '.join([str(j) for j in state[i]]) for i in range(3)]
    return ', '.join(s).strip()

def state_step(n, state, x, s):
    # Initiate list to contain any movable stacks
    stack = []
    # Initiate current variable to store current peg position
    current = None
    next_num = 0
    sequence = []
    # Only check and create stack if it is possible to move the stack
    if x % 2 == 1:
        # Check for existence of movable stack
        for i, sublist in enumerate(state):
            sublist_set = set(sublist)  # Convert the sublist to a set for efficient lookups
            current_num = 1    

            # Check for possible sequences starting with 1
            while current_num in sublist_set and (2**current_num-1) <= s:
                sequence.append(current_num)
                current_num += 1

            # Build stack if there are at least 2 sequential disks
            if len(sequence) >= 2:
                stack = sequence
                current = i
                next_num = stack[-1] + 1
                ahead = 1 if stack[-1] % 2 == 1 else -1
                break
            
    # Check if valid stack available to be moved
    if x % 2 == 1 and len(stack) > 0 and (s - (2**stack[-1]-2)) >= 0:#and state[(current + ahead) % 3][0] == next_num
        # Update move count based on stack height - reduce s by number of moves +1 as recursive call further reduces s by 1
        # Number of moves needed to move a stack is 2^(n)-1, where n is largest disk in stack
        s -= 2**stack[-1]-2
        stack.reverse()
        # Move stack
        for item in stack:
            state[current].remove(item)
            state[(current + ahead) % 3].insert(0, item)
    # If no stack available to be moved, try moving disk 1
    elif x % 2 == 1:
        current = next((index for index, sublist in enumerate(state) if len(sublist) > 0 and sublist[0] == 1), None)
        ahead = 1
    # If disk 1 not available to be moved, try moving next smallest disk, break recursion if no legal moves found
    else:
        # Returns a list of lists where each lists contains index of list and first member in that lists (exclude smallest disk)
        filtered_values = [(i, lst[0]) for i, lst in enumerate(state) if lst and lst[0] != 1]
        current, k = min(filtered_values, key=lambda x: x[1])
        ahead = 1 if k % 2 == 1 else -1
        # If target peg is not empty and smallest disk on target peg is smaller than k, move is illegal, break out of recursion
        if state[(current + ahead) % 3]:
            if state[(current + ahead) % 3][0] < k:
                return
    # Move a single disk if no stack was moved
    if len(stack)==0:
        disk = state[current].pop(0)
        state[(current + ahead) % 3].insert(0, disk)

    # Check if list has reached end state, break recursion if yes
    if s <= 0 or state == [list(range(1, n+1)), [], []] or state == [[], list(range(1, n+1)), []] or state == [[], [], list(range(1, n+1))]:
        return

    state_step(n, state, x + 1, s - 1)

def tower_hanoi(n, state):
    global mm
    # Determine peg position of largest disk
    n_pos = [i for i, sublist in enumerate(state) if n in sublist]
    input_state = copy.deepcopy(state)
    
    # Bring current state to end state assuming moving smallest disk is the correct next move
    state_step(n, state, 1, 2**n)

    # if all pegs successfully moved to destination peg
    if state == [list(range(1, n+1)), [], []] or state == [[], list(range(1, n+1)), []] or state == [[], [], list(range(1, n+1))]:
        state_step(n, input_state, 1, mm-1)
        # Find destination peg
        end_pos = next((i for i, sublist in enumerate(state) if sublist), None) if any(sublist for sublist in state) else None

        if n%2==1:
            origin = (end_pos-1)%3
        else:
            origin = (end_pos+1)%3

        origin_mapping = {0: 'A', 1: 'B', 2: 'C'}
        origin = origin_mapping.get(origin, None)
        formatted_state = f"{origin}, {state_to_str(input_state)}"
        return formatted_state
    else:
        # Reinitiate input_state and step through to completion assuming that moving 1 is not the first legal move
        state = copy.deepcopy(input_state)
        state_step(n, state, 2, 2**n)

        if state == [list(range(1, n+1)), [], []] or state == [[], list(range(1, n+1)), []] or state == [[], [], list(range(1, n+1))]:
            state_step(n, input_state, 2, mm-1)
            # Find destination peg
            end_pos = next((i for i, sublist in enumerate(state) if sublist), None) if any(sublist for sublist in state) else None

            if n%2==1:
                origin = (end_pos-1)%3
            else:
                origin = (end_pos+1)%3

            origin_mapping = {0: 'A', 1: 'B', 2: 'C'}
            origin = origin_mapping.get(origin, None)
            formatted_state = f"{origin}, {state_to_str(input_state)}"
            return formatted_state
        else:
            return 'impossible'
        
num_case = int(sys.stdin.readline())
for _ in range(num_case):
    s = sys.stdin.readline().split(',')
    state, mm = [[int(r) for r in t.split()] for t in s[:3]], int(s[3])
    n = len(state[0]) + len(state[1]) + len(state[2])
    print(tower_hanoi(n, state))
