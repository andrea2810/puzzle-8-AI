import time
import timeit
from collections import deque
from random import randint
import numpy as np


#/**********************CLASS PUZZLE**********************/
class PuzzleState:
    def __init__(self, state, parent, move, depth, cost, key):
        self.state = state #Board
        self.parent = parent
        self.move = move 
        self.depth = depth
        self.cost = cost
        self.key = key
        if self.state:
            #String format the board
            self.map = ''.join(str(e) for e in self.state)
    def __eq__(self, other):
        return self.map == other.map
    def __lt__(self, other):
        return self.map < other.map
    def __str__(self):
        return str(self.map)

#/********************GLOBAL VARIABLES********************/
GoalState = [0, 1, 2, 3, 4, 5, 6, 7, 8]
GoalNode = None #At finding solution
NodesExpanded = 0 #Total nodes visited
MaxSearchDeep = 0 #Max Deep
MaxFrontier = 0 #Max Frontier

#/********************SEARCH BY WIDTH*********************/
def searchByWidth(initialBoard):
    global MaxFrontier, GoalNode, MaxSearchDeep

    boardVisited= set()
    Queue = deque([PuzzleState(initialBoard, None, None, 0, 0, 0)])

    while Queue:
        node = Queue.popleft()
        boardVisited.add(node.map)
        if node.state == GoalState:
            while True:
                try:
                    if node:
                        GoalNode = node
                        break
                    else:
                        raise Exception
                except Exception as wrongValue:
                    print('The value of the node is not valid')
            return Queue
        posiblePaths = subNodes(node)
        for path in posiblePaths:
            if path.map not in boardVisited:
                Queue.append(path)
                boardVisited.add(path.map)
                if path.depth > MaxSearchDeep:
                    MaxSearchDeep = MaxSearchDeep + 1
        if len(Queue) > MaxFrontier:
            QueueSize = len(Queue)
            MaxFrontier = QueueSize


#/*********************SEARCH BY DEEP*********************/
def searchByDeep(initialBoard):
    global MaxFrontier, GoalNode, MaxSearchDeep

    boardVisited = set()
    stack = list([PuzzleState(initialBoard, None, None, 0, 0, 0)])
    while stack:
        node = stack.pop()
        boardVisited.add(node.map)
        if node.state == GoalState:
            while True:
                try:
                    if node:
                        GoalNode = node
                        break
                    else:
                        raise Exception
                except Exception as wrongValue:
                    print('The value of the node is not valid')
            return stack
        #inverse the order of next paths for execution porpuses
        posiblePaths = reversed(subNodes(node))
        for path in posiblePaths:
            if path.map not in boardVisited:
                stack.append(path)
                boardVisited.add(path.map)
                if path.depth > MaxSearchDeep:
                    MaxSearchDeep = 1 + MaxSearchDeep
        if len(stack) > MaxFrontier:
            MaxFrontier = len(stack)


#/*********************SEARCH BY DEEP*********************/
def searchByIteratedDeep(initialBoard):
    global MaxFrontier, GoalNode, MaxSearchDeep
    
    
    #transform initial state to calculate Heuritic
    node1 = ""
    for poss in initialBoard:
        node1 = node1 + str(poss)

    #calculate Heuristic and set initial node
    key = Heuristic(node1)
    boardVisited= set()
    Queue = []
    Queue.append(PuzzleState(initialBoard, None, None, 0, 0, key)) 
    boardVisited.add(node1)
    
    while Queue:
        Queue.sort(key=lambda o: o.key) 
        node = Queue.pop(0)
        if node.state == GoalState:
            GoalNode = node
            return Queue
        posiblePaths = subNodes(node)
        for path in posiblePaths:      
            thisPath = path.map[:]
            if thisPath not in boardVisited:
                key = Heuristic(path.map)
                path.key = key + path.depth
                Queue.append(path)               
                boardVisited.add(path.map[:])
                if path.depth > MaxSearchDeep:
                    MaxSearchDeep = 1 + MaxSearchDeep
                
#Heuristic: distance to root numbers
values_0 = [0,1,2,1,2,3,2,3,4]
values_1 = [1,0,1,2,1,2,3,2,3]
values_2 = [2,1,0,3,2,1,4,3,2]
values_3 = [1,2,3,0,1,2,1,2,3]
values_4 = [2,1,2,1,0,1,2,1,2]
values_5 = [3,2,1,2,1,0,3,2,1]
values_6 = [2,3,4,1,2,3,0,1,2]
values_7 = [3,2,3,2,1,2,1,0,1]
values_8 = [4,3,2,3,2,1,2,1,0]


def Heuristic(node):

    global values_0,values_1,values_2,values_3,values_4,values_5,values_6,values_7,values_8   
    v0=values_0[node.index("0")]
    v1=values_1[node.index("1")]
    v2=values_2[node.index("2")]
    v3=values_3[node.index("3")]
    v4=values_4[node.index("4")]
    v5=values_5[node.index("5")]
    v6=values_6[node.index("6")]
    v7=values_7[node.index("7")]
    v8=values_8[node.index("8")]
    valorTotal = v0+v1+v2+v3+v4+v5+v6+v7+v8
    return valorTotal

#/***********************SUBNODES*************************/
def subNodes(node):
    global NodesExpanded

    actions = {0: {'Down', 'Right'},
                1: {'Down', 'Right', 'Left'},
                2: {'Down', 'Left'},
                3: {'Up', 'Down', 'Right'},
                4: {'Up', 'Down', 'Right', 'Left'},
                5: {'Up', 'Down', 'Left'},
                6: {'Up', 'Right'},
                7: {'Up', 'Right', 'Left'},
                8: {'Up', 'Left'}}

    NodesExpanded += 1

    #import pdb; pdb.set_trace()

    nextPaths = []
    index = node.state.index(0)
    #nodes = []
    for action in actions[index]:
        nextPaths.append(PuzzleState(
            move(node.state, action), #NewState/Board with a new move
            node, #ParentNode
            action, #Move
            node.depth + 1, #Depth
            node.cost + 1, #Cost
            0)) #key
    return nextPaths


#/**************************MOVE**************************/
def move(board, direction):
    #Make a copy of state
    newState = board[:]
    #Get the index of element 0
    index = newState.index(0)

    #Swap elements
    if direction == 'Up':
        newState[index], newState[index - 3] = newState[index - 3], \
            newState[index]
    elif direction == 'Down':
        newState[index], newState[index + 3] = newState[index + 3], \
            newState[index]
    elif direction == 'Right':
        newState[index], newState[index + 1] = newState[index + 1], \
            newState[index]
    elif direction == 'Left':
        newState[index], newState[index - 1] = newState[index - 1], \
            newState[index]

    return newState


#/*****************CREATE RANDOM PUZZLE8******************/
def makeRandomBoard():
    puzzle = [9,9,9,9,9,9,9,9,9]
    for x in range(9):
        num = randint(0, 8)
        while num in puzzle:
            num = randint(0,8)
        puzzle[x] = num

    return puzzle

#/**************************MAIN*************************/
def main():

    global GoalNode, MaxSearchDeep, MaxFrontier, NodesExpanded

    initialBoard = makeRandomBoard()
    print(initialBoard)

    for i in range(0, 3):
        # Clear variables
        NodesExpanded = 0
        MaxSearchDeep = 0
        MaxFrontier = 0

        #Start timer to know how long each method takes 
        start = timeit.default_timer()
        if i == 0:
            searchByWidth(initialBoard)
        elif i == 1:
            searchByDeep(initialBoard)
        else:
            searchByIteratedDeep(initialBoard)

        stop = timeit.default_timer()
        time = stop-start
        #import pdb; pdb.set_trace()
        
        while True:
            try:
                if GoalNode:
                    deep = GoalNode.depth
                    moves = []
                    while initialBoard != GoalNode.state:
                        moves.insert(0, GoalNode.move)
                        GoalNode = GoalNode.parent

                    print('Path: ',moves)
                    print('Final Cost: ',len(moves))
                    print('Nodes Expanded: ',str(NodesExpanded))
                    print('Search depth: ',str(deep))
                    print('MaxSearchDeep: ',str(MaxSearchDeep))
                    print('Running Time: ',format(time, '.8f'))
                    input('Please, enter any key to continue')
                    break
                else:
                    raise Exception
            except Exception as wrongValue:
                print('The value of the nodeGoal is not valid')


if __name__ == '__main__':
    main()

