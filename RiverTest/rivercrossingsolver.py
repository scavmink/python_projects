import networkx as nx
from matplotlib import pyplot as plt
from itertools import combinations, permutations
from graphviz import Digraph
from string import uppercase
import os

debug = False

# Needed for access to dot program
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

# setup global variables
goalNode = 0        # the node in which the goal state is achieved
prevNode = 0        # previous node number
currNode = 1        # current node number
currLevel = 1       # the current level within the hierarchy
goalReached = False # tag to stop search

# setup game variables
Graph = nx.DiGraph()
leftBankStatus = []
rightBankStatus = []
players = []
drivers = []
passengers = []
goalStatus = []
boatCapacity = 2 # Default value for most river crossing games
invalidBank = [] # Stores a list of bank statuses that are forbidden
invalidBoat = [] # Stores a list of boat statuses that are forbidden
timeLimit = 0
timeValues = {}
currTime = 0
duplicateNodes = False

#==========================================================================
# FUNCTIONS
#==========================================================================
def setPlayers(s):
    global players
    players = set(s.split())

def startLeft():
    global players
    global leftBankStatus
    if players != []:
        leftBankStatus = players

def setleftBankStatus(s):
    global leftBankStatus
    leftBankStatus = set(s.split())

def setrightBankStatus(s):
    global rightBankStatus
    rightBankStatus = set(s.split())

def setgoalStatus(s1, s2):
    global goalStatus
    goalStatus = [set(s1.split()), set(s2.split())]

def setdrivers(s):
    global drivers
    drivers = set(s.split())

def setinvalidBoat(s):
    global invalidBoat
    invalidBoat = [x.split(",") for x in s.split()]

def setinvalidBank(s):
    global invalidBank
    invalidBank = [x.split(",") for x in s.split()]

def setboatCapacity(d):
    global boatCapacity
    boatCapacity = d

def settimeLimit(d):
    global timeLimit
    timeLimit = d

def settimeValues(s):
    global timeValues
    pairs = s.split()
    for pair in pairs:
        k, v = pair.split(":")
        timeValues[k] = int(v)

def setduplicateNode(b=False):
    global duplicateNodes
    duplicateNodes = b


def checkSettings():
    pass

# check for invalid bank status or invalid boat status
def isInvalid(currStatus, checkStatus):
    for bs in currStatus:
        if sorted(bs) == sorted(checkStatus):
            return False
    return True

# generate a list of boat combinations, eliminating any entries that have no driver
def generateBoatCombinations(bankStatus, override=0):
    boatCombos = []
    if override > 0:
        combos = combinations(bankStatus,override)
        for combo in combos:
            # use an intersection to determine if there is at least one driver in the combo
            test = set(combo).intersection(drivers)
            # if there are no drivers, the list should be empty
            if len(test) > 0:
                boatCombos.append(list(combo))
    else:
        for i in range(boatCapacity):
            combos = combinations(bankStatus,i+1)
            for combo in combos:
                # use an intersection to determine if there is at least one driver in the combo
                test = set(combo).intersection(drivers)
                # if there are no drivers, the list should be empty
                if len(test) > 0:
                    boatCombos.append(list(combo))
    return boatCombos

# validate the combinations by checking the following
# - remove invalid boat statuses
# - remove invalid bank statuses
def validate(bankStatus, level):
    global leftBankStatus
    global rightBankStatus
    # make a copy of the bank status
    bankStatus_ = bankStatus[:]
    for bs in bankStatus_:
        # remove invalid boat combos
        if not isInvalid(invalidBoat, bs):
            bankStatus.remove(bs)
            continue
        # left side level is odd, right side is even (mod 2)
        if level % 2 == 0:
            leftTempBank = list(set(leftBankStatus) - set(bs))  # removes combo from left bank
            if not isInvalid(invalidBank, leftTempBank):        # if that's invalid
                bankStatus.remove(bs)
                continue
            rightTempBank = list(rightBankStatus) + bs
            if not isInvalid(invalidBank, rightTempBank):
                bankStatus.remove(bs)
        else:
            rightTempBank = list(set(rightBankStatus) - set(bs))  # removes combo from left bank
            if not isInvalid(invalidBank, rightTempBank):  # if that's invalid
                bankStatus.remove(bs)
                continue
            leftTempBank = leftBankStatus + bs
            if not isInvalid(invalidBank, leftTempBank):
                bankStatus.remove(bs)
    return bankStatus

# if the move is valid, add the node (as long as it doesn't already exist
def addNode(leftBank, rightBank, level, boat):
    global Graph
    global goalReached
    global currNode
    global prevNode
    global goalNode
    global goalStatus
    # look for existing nodes with the same bank status
    existing = filter(
        lambda (k, v):
            set(v["leftBank"]) == set(leftBank) and
            set(v["rightBank"]) == set(rightBank) and
            int(v["level"]) % 2 == (level + 1) % 2,
        Graph.nodes(data=True)
    )
    timeAdd = 0
    if len(existing) == 0:  # no nodes found
        Graph.add_node(currNode, leftBank=leftBank, rightBank=rightBank, level=level + 1)
        Graph.add_edge(prevNode, currNode, label=",".join(boat))
        currNode += 1
        if (goalStatus[0] == set(leftBank) and goalStatus[1] == set(rightBank)):
            goalReached = True
            goalNode = currNode - 1


def solve_time(fname=None):
    global goalNode
    orgleftBank = []
    orgrightBank = []
    orgleftBank = timeValues.items()
    currNode = 1
    goalTimes = {}


    def pp(pre, d, left, right, total):
        return "\t" * (d - 1) + pre + "[" + ",".join([str(l[1]) for l in left]) + "] [" + ",".join(
            [str(r[1]) for r in right]) + "] = " + str(total)

    def nodeLabel(left, right):
        return "[" + ",".join([str(l[1]) for l in sorted(left)]) + "] [" + ",".join(
            [str(r[1]) for r in sorted(right)]) + "]"

    def recursive(leftBank, rightBank, prevNode, rTotal, depth=1):
        global currNode
        pairs = combinations(leftBank, 2)
        for pair in pairs:
            # Get highest value from pair
            timeCrossed = max(pair[0][1], pair[1][1])
            rTotal += timeCrossed
            # move pair to right bank
            templeftBank = list(set(leftBank) - set(pair))
            temprightBank = rightBank + list(pair)
            # create node and edge from previous node
            # newNode = nodeLabel(templeftBank, temprightBank)
            newNode = currNode + 1
            nodelbank = [x[0] for x in templeftBank]
            noderbank = [x[0] for x in temprightBank]
            Graph.add_node(newNode, leftBank=nodelbank, rightBank=noderbank)
            Graph.add_edge(prevNode, newNode, weight=timeCrossed)
            currNode += 1

            # print pp(">>>", depth, templeftBank, temprightBank, rTotal)

            if len(templeftBank) > 0:
                # return player with lowest value
                rplayer = min(temprightBank, key=lambda x: x[1])
                timeReturned = rplayer[1]
                rTotal += timeReturned
                # move return player to left bank
                temprightBank.remove(rplayer)
                templeftBank.append(rplayer)
                # create node and edge
                # newNode2 = nodeLabel(templeftBank, temprightBank)
                newNode2 = currNode + 1
                nodelbank = [x[0] for x in templeftBank]
                noderbank = [x[0] for x in temprightBank]
                Graph.add_node(newNode2, leftBank=nodelbank, rightBank=noderbank)
                Graph.add_edge(newNode, newNode2, weight=timeReturned)
                currNode += 1

                # print pp("<<<", depth, templeftBank, temprightBank, rTotal)
                recursive(templeftBank, temprightBank, newNode2, rTotal, depth + 1)
                rTotal -= (timeCrossed + timeReturned)
            else: # if completed, log the goal node
                goalTimes.update({newNode:rTotal})

    # homeNode = nodeLabel(orgleftBank, orgrightBank)
    homeNode = currNode
    nodelbank = [x[0] for x in orgleftBank]
    noderbank = [x[0] for x in orgrightBank]
    Graph.add_node(homeNode, leftBank=nodelbank, rightBank=noderbank)
    currNode += 1
    recursive(orgleftBank, orgrightBank, homeNode, 0)

    goalNode = min(goalTimes.items(), key=lambda x: x[1])[0]
    # print str(goalNode)
    output(fname)


def solve(fname=None):
    # If it's a time-based puzzle, use the other function
    if timeLimit > 0:
        solve_time(fname)
        return
    global goalNode
    global prevNode
    global currNode
    global currLevel
    global goalReached
    global Graph
    global leftBankStatus
    global rightBankStatus
    global players
    global drivers
    global passengers
    global goalStatus
    global boatCapacity
    global invalidBank
    global invalidBoat

    #==========================================================================
    # GENERATE NODES
    #==========================================================================

    # Create starting node 0
    Graph.add_node(currNode, leftBank=leftBankStatus, rightBank=rightBankStatus, level=0)
    currNode += 1
    prevNode += 1

    level = 0
    # Loop until we reach our goal status
    while (not goalReached):
        # get all nodes at current level
        level_nodes = filter(lambda (k, v): v['level'] == level, Graph.nodes(data=True))

        for level_node in level_nodes:
            prevNode = level_node[0] # If a new node is created, this is the previous one
            leftBankStatus = level_node[1]['leftBank']
            rightBankStatus = level_node[1]['rightBank']

            if level % 2 == 0:  # For even rows, the boat is on the left bank
                temp = generateBoatCombinations(leftBankStatus)
                temp = validate(temp, level)
                for new_node in temp:
                    new_leftBank = list(set(leftBankStatus) - set(new_node))
                    new_rightBank = list(rightBankStatus) + new_node
                    addNode(new_leftBank, new_rightBank, level, new_node)
            else:
                temp = generateBoatCombinations(rightBankStatus)
                temp = validate(temp, level)
                for new_node in temp:
                    new_leftBank = list(leftBankStatus) + new_node
                    new_rightBank = list(set(rightBankStatus) - set(new_node))
                    addNode(new_leftBank, new_rightBank, level, new_node)
        level += 1
        if level > 20:
            goalNode = prevNode
            break
    output(fname)
    #==========================================================================
    # OUTPUT AND DRAWING
    #==========================================================================

def output(fname):
        #get shortest path
        shortest_path = nx.shortest_path(Graph, source=1, target=goalNode)
        shortest_path_edges = zip(shortest_path, shortest_path[1:])

        prevL = []
        for node in shortest_path:
            currL = Graph.node[node]["leftBank"]
            currR = Graph.node[node]["rightBank"]
            if node != 1:
                if len(prevL) > len(currL):
                    boat = set(prevL) - set(currL)
                else:
                    boat = set(currL) - set(prevL)
                lbank = ",".join(currL)
                rbank = ",".join(currR)
                node_name = lbank + "|   << " + ",".join(boat) + " >>   |" + rbank
                print node_name
            prevL = currL


        if type(fname) is not None:

            dot = Digraph(format="png")
            for node in range(1, goalNode+1):
                # for node in shortest_path:
                lbank = ",".join(Graph.node[node]["leftBank"])
                rbank = ",".join(Graph.node[node]["rightBank"])
                node_name = "|-|".join([lbank,rbank])

                # print node, node_name
                dot.node(str(node), node_name)

            for e in Graph.edges():
                if (e[0],e[1]) in shortest_path_edges:
                    dot.edge(str(e[0]), str(e[1]), color="red")
                else:
                    dot.edge(str(e[0]), str(e[1]), color="black")
            dot.render(fname)

def main_debug():

    # Farmer one
    setPlayers("Farmer Wolf Goat Cabbage")
    setdrivers("Farmer")
    setinvalidBoat("")
    setinvalidBank("Wolf,Goat Goat,Cabbage Wolf,Goat,Cabbage")
    setboatCapacity(2)

def main():

    input_players = raw_input("Enter players (separate by space) : ")
    setPlayers(input_players)

    input_sameside = raw_input("Do all players start on the left bank? Y/N : ")
    if input_sameside == "Y" or input_sameside == "y":
        setleftBankStatus(input_players)
        setgoalStatus("",input_players)
    elif input_sameside == "N" or input_sameside == "n":
        input_bankplayers = (raw_input("Enter players on left bank and right bank (CSV lists separate by space) :"))
        banks = input_bankplayers.split()
        setleftBankStatus(banks[0])
        setrightBankStatus(banks[1])
        input_goalstatus = raw_input("Enter goal status for both banks (CSV lists separate by space) : ")
        goals = input_goalstatus.split()
        setgoalStatus(goals[0], goals[1])

    input_drivers = raw_input("Select drivers (separate by space) : ")
    setdrivers(input_drivers)

    input_invalidboat = raw_input("Enter combinations of invalid boat users (CSV lists separated by space) : ")
    setinvalidBoat(input_invalidboat)

    input_invalidbank = raw_input("Enter combinations of invalid bank status (CSV lists separated by space) : ")
    setinvalidBank(input_invalidbank)

    input_boatcapacity = int(raw_input("Enter max number of boat passengers (Default: 2) : "))
    setboatCapacity(input_boatcapacity)

if __name__ == "__main__" and debug == False:
    main()
    solve()
elif __name__ == "__main__" and debug == True:
    main_debug()
    solve()
