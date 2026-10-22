import random
import heapq

goal=[0,1,2,3,4,5,6,7,8]

def is_goal(puzzle):
    if puzzle==goal:
        return True
    else:
        return False
    
def create_random_puzzle():
    l=[1,2,3,4,5,6,7,8,0]
    random.shuffle(l)
    return l

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

def hamming(puzzle):
    misplaced=0
    for i in range(len(puzzle)):
        if puzzle[i]!=goal[i] and puzzle[i]!=0:
            misplaced+=1
        else:
            pass
    return misplaced

def get_position(index):
    row=index//3
    column=index%3
    return row,column

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

def get_neighbors(puzzle):
    neighbors=[]
    zero_i=puzzle.index(0)
    row,column=get_position(zero_i)
    if row>0:
        new_puzzle=puzzle.copy()
        temp=new_puzzle[zero_i]
        new_puzzle[zero_i]=new_puzzle[zero_i-3]
        new_puzzle[zero_i-3]=temp
        neighbors.append(new_puzzle)
    if row<2:
        new_puzzle=puzzle.copy()
        temp=new_puzzle[zero_i]
        new_puzzle[zero_i]=new_puzzle[zero_i+3]
        new_puzzle[zero_i+3]=temp
        neighbors.append(new_puzzle)
    if column>0:
        new_puzzle=puzzle.copy()
        temp=new_puzzle[zero_i]
        new_puzzle[zero_i]=new_puzzle[zero_i-1]
        new_puzzle[zero_i-1]=temp
        neighbors.append(new_puzzle)
    if column<2:
        new_puzzle=puzzle.copy()
        temp=new_puzzle[zero_i]
        new_puzzle[zero_i]=new_puzzle[zero_i+1]
        new_puzzle[zero_i+1]=temp
        neighbors.append(new_puzzle)
    return neighbors

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

class Node:
    def __init__(self):
        self.state = []
        self.previous_node = 0
        self.total_cost = 0
        self.heuristic_cost = 0

def astar(start_puzzle, heuristic_function, print_result):
    explored = []
    priority_queue = []
    backup_counter = 0 #this is only to fix a bug where the heapqueue crashes if it is sorting 2 nodes with the same total_cost
    
    #each whole board is a node, and the next move is how the whole board would look like next
    
    if(not is_solvable(start_puzzle)):
        print("puzzle is not solvable!")
        return
    
    start_node = Node()
    start_node.state = start_puzzle.copy()
    
    current_node = start_node
    
    while not is_goal(current_node.state):
        neighbor_states = get_neighbors(current_node.state)
    
        for new_state in neighbor_states:
            new_node = Node()
            new_node.state = new_state
            new_node.previous_node = current_node
            new_node.total_cost = current_node.total_cost + 1
            new_node.heuristic_cost = new_node.total_cost + heuristic_function(new_node.state)
            
            heapq.heappush(priority_queue, (new_node.heuristic_cost, backup_counter, new_node))
            backup_counter += 1
            
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
                
    #build the optimal path through starting in the goal_puzzle-node and walking backwards through the previous-nodes
    shortest_path = []
    total_cost = current_node.total_cost
    while current_node.previous_node != 0:
        #add the previous node to the front of the list to get it in the correct order
        shortest_path.insert(0, current_node)
        #shortest_path.append(current_node)
        current_node = current_node.previous_node
        
    #since while loop stops before adding the first node, I'll just add it here
    shortest_path.insert(0, current_node)
    #shortest_path.append(current_node)
    
    if print_result:
        move = 0
        print("Heusistic function: " + str(heuristic_function))
        print("---------------START---------------")
        for node in shortest_path:
            print("Move " + str(move) + ": " + str(node.state))
            move += 1
        
    print("Total cost: " + str(total_cost))
    return shortest_path

if __name__ == "__main__":
    test_puzzle = [7, 2, 4, 5, 0, 6, 8, 3, 1]
    random_puzzle = create_random_puzzle()
    
    shortest_path = astar(random_puzzle, manhattan, True)