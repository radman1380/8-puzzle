import random
import heapq
goal=[1,2,3,4,5,6,7,8,0]
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


