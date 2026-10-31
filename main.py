import random
import heapq
import time
import statistics
goal=[0,1,2,3,4,5,6,7,8]

# Function: Checks whether the puzzle matches the goal state.
# Input: puzzle — a list containing the current board.
# Output: True if the puzzle matches the goal; otherwise False.
def is_goal(puzzle):
    if puzzle==goal:
        return True
    else:
        return False


# Function: Creates a random board by shuffling the tiles and blank.
# Input: None.
# Output: A list containing tiles 1–8 and the blank (0).
# Note: The generated puzzle is not necessarily solvable.

def create_random_puzzle():
    l=[1,2,3,4,5,6,7,8,0]
    random.shuffle(l)
    return l

# Function: Checks solvability by counting inversions, ignoring the blank.
# An inversion occurs when a larger tile appears before a smaller tile.
# For this 3x3 board and goal, an even inversion count means solvable.
# Input: puzzle — a list containing the current board.
# Output: True if the puzzle is solvable; otherwise False.

def is_solvable(puzzle):
    inversion=0
    for i in range(len(puzzle)):
        for j in range(i+1,len(puzzle)):
            if puzzle[i]!=0 and puzzle[j]!=0 and puzzle[i]>puzzle[j]:
                inversion=inversion+1
    if inversion%2==0:
        return True
    else:
        return False


# Function: Calculates the Hamming heuristic by counting misplaced tiles.
# The blank (0) is excluded.
# Input: puzzle — a list containing the current board.
# Output: The number of numbered tiles outside their goal positions.

def hamming(puzzle):
    misplaced=0
    for i in range(len(puzzle)):
        if puzzle[i]!=goal[i] and puzzle[i]!=0:
            misplaced+=1
        else:
            pass
    return misplaced
# Function: Converts a list index into a row and column on the 3x3 board.
# Input: index — an integer from 0 to 8.
# Output: A tuple containing (row, column), both numbered from 0.

def get_position(index):
    row=index//3
    column=index%3
    return row,column

# Function: Calculates the Manhattan heuristic.
# Adds the horizontal and vertical distances between each numbered
# tile's current position and its goal position. The blank is excluded.
# Input: puzzle — a list containing the current board.
# Output: The sum of the distances for all numbered tiles.

def manhattan(puzzle):
    distance=0
    for i in range(len(puzzle)):
        if puzzle[i]==0:
            pass
        else:
            current_position=get_position(i)
            goal_position=get_position(goal.index(puzzle[i]))
            distance+=abs(current_position[0]-goal_position[0])+abs(current_position[1]-goal_position[1])

    return distance


def no_heuristic(puzzle):
    return 0

# Function: Generates all boards reachable by one legal blank movement.
# The blank can move up, down, left, or right within the board boundaries.
# Each movement swaps the blank with the adjacent numbered tile.
# Input: puzzle — a list containing the current board.
# Output: A list of neighboring boards. The input board is unchanged.

def get_neighbors(puzzle):
    neighbors=[]
    zero_i=puzzle.index(0)
    row,column=get_position(zero_i)
    if row>0: #move the blanl up
        new_puzzle=puzzle.copy()
        temp=new_puzzle[zero_i]
        new_puzzle[zero_i]=new_puzzle[zero_i-3]
        new_puzzle[zero_i-3]=temp
        neighbors.append(new_puzzle)
    if row<2: # move the blank down
        new_puzzle=puzzle.copy()
        temp=new_puzzle[zero_i]
        new_puzzle[zero_i]=new_puzzle[zero_i+3]
        new_puzzle[zero_i+3]=temp
        neighbors.append(new_puzzle)
    if column>0: #move the blank left
        new_puzzle=puzzle.copy()
        temp=new_puzzle[zero_i]
        new_puzzle[zero_i]=new_puzzle[zero_i-1]
        new_puzzle[zero_i-1]=temp
        neighbors.append(new_puzzle)
    if column<2: #move the blank right
        new_puzzle=puzzle.copy()
        temp=new_puzzle[zero_i]
        new_puzzle[zero_i]=new_puzzle[zero_i+1]
        new_puzzle[zero_i+1]=temp
        neighbors.append(new_puzzle)
    return neighbors

# Function: Generates the requested number of distinct solvable puzzles.
# Random boards are rejected if unsolvable or already collected.
# Input: count — the number of puzzles to generate; default is 100.
# Output: A list of distinct solvable puzzle boards.

def generate_solvable_puzzles(count=100):
    puzzles = []
    seen = set()
    while len(puzzles) < count:
        puzzle = create_random_puzzle()
        state = tuple(puzzle)

        if is_solvable(puzzle) and state not in seen:
            puzzles.append(puzzle)
            seen.add(state)

    return puzzles

# Function: Represents one board and its associated search information.
# Input: No constructor arguments; attributes are assigned during search.
# Output: A Node object containing:
#   state — the current board.
#   previous_node — the parent node, or 0 for the starting node.
#   total_cost — moves made from the start (g).
#   heuristic_cost — search priority, calculated as g + h.

class Node:
    def __init__(self):
        self.state = []
        self.previous_node = 0
        self.total_cost = 0
        self.heuristic_cost = 0

#Description: Finds the shortest path between 2 nodes, in this case the least amount of moves to get from the start puzzle to the goal puzzle.
#Input: Takes a start puzzle, a heuristic function and a true/false variabel if you want to print the shortest path list or not.
#Output: returns the shortest path list with the most efficient moves, and the number of expanded nodes
def astar(start_puzzle, heuristic_function, print_result):
    explored = []
    priority_queue = []
    backup_counter = 0 #This is only to fix a bug where the heapqueue crashes if it is sorting 2 nodes with the same total_cost
    expanded_nodes=0
    
    
    #Create start node with the start puzzle
    start_node = Node()
    start_node.state = start_puzzle.copy()
    
    current_node = start_node
    
    #Loop until goal state has been reached
    while not is_goal(current_node.state):
        expanded_nodes+=1
        neighbor_states = get_neighbors(current_node.state) #Get all possible next states (neighbors) from current node
    
        #Each neghboring state becomes a new node and get its estimated total cost calculated with a heuristic.
        #Then it gets sorted into the priority-heapqueue
        for new_state in neighbor_states:
            new_node = Node()  #creates a node for each neighbor
            new_node.state = new_state
            new_node.previous_node = current_node
            new_node.total_cost = current_node.total_cost + 1
            new_node.heuristic_cost = new_node.total_cost + heuristic_function(new_node.state)
            
            heapq.heappush(priority_queue, (new_node.heuristic_cost, backup_counter, new_node))
            backup_counter += 1
            
        #Find the cheapest unexplored node in the priority-heapqueue, that becomes the next current node
        found_unexplored_node = False
        while len(priority_queue) > 0 and not found_unexplored_node:
            next_node = heapq.heappop(priority_queue)[2]
            
            already_explored = False
            for explored_node in explored:
                if next_node.state == explored_node.state:
                    already_explored = True
                    
            if not already_explored:
                found_unexplored_node = True
                explored.append(next_node)
                current_node = next_node
                
    #Build the optimal path through starting in the goal_puzzle-node and walking backwards through the previous-nodes
    shortest_path = []
    total_cost = current_node.total_cost
    while current_node.previous_node != 0:
        #Add the previous node to the front of the list to get it in the correct order
        shortest_path.insert(0, current_node)
        current_node = current_node.previous_node
        
    #Since while loop stops before adding the first node, we'll just add it here
    shortest_path.insert(0, current_node)
    
    if print_result:
        move = 0
        print("Heusistic function: " + str(heuristic_function))
        print("---------------START---------------")
        for node in shortest_path:
            print("Move " + str(move) + ": " + str(node.state))
            move += 1
        
        print("Total cost: " + str(total_cost))
        
    return shortest_path,expanded_nodes

if __name__ == "__main__":
    # Generate once so both heuristics use the same 100 puzzles.
    puzzles = generate_solvable_puzzles(count=100)

    results = {
        "Hamming": [],
        "Manhattan": []
    }

    for heuristic_name, heuristic_function in [
        ("Hamming", hamming),
        ("Manhattan", manhattan)
    ]:
        for puzzle_number, puzzle in enumerate(puzzles, start=1):
            start_time = time.perf_counter()

            shortest_path, expanded_nodes = astar(
                puzzle, heuristic_function, False
            )

            execution_time = time.perf_counter() - start_time

            results[heuristic_name].append({
                "puzzle_number": puzzle_number,
                "execution_time": execution_time,
                "expanded_nodes": expanded_nodes
            })

            # Print after timing so progress output isn't measured.
            print(
                f"{heuristic_name} | Puzzle {puzzle_number}/100 | "
                f"Time: {execution_time:.6f} seconds | "
                f"Expanded nodes: {expanded_nodes}"
            )
    print("\nSummary of 100 puzzles per heuristic")

    for heuristic_name, measurements in results.items():
        times = [run["execution_time"] for run in measurements]
        expansions = [run["expanded_nodes"] for run in measurements]

        print(f"\n{heuristic_name}")
        print(f"Mean runtime: {statistics.mean(times):.6f} seconds")
        print(f"Runtime standard deviation: {statistics.stdev(times):.6f} seconds")
        print(f"Mean expanded nodes: {statistics.mean(expansions):.2f}")
        print(f"Expanded nodes standard deviation: {statistics.stdev(expansions):.2f}")