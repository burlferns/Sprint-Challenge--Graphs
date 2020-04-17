from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from util import Stack, Queue  # These may come in handy

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
roomGraph = {}

###############################################################################
# This function populates the key/value pair in the roomGraph for the current
# room. The key is the room, and the value is a dictionary of direction keys and 
# a value neighbor rooms that are in the particular direction
###############################################################################  
def getAdjoinRoom():
    # room is the one for which we want to find the direction and rroom neighbors 
    room = player.current_room.id 

    roomExits = player.current_room.get_exits()
    goBackInfo = {'n':'s', 'e':'w', 's':'n', 'w':'e'}
    roomGraph[room] = {}
    for direction in roomExits:
        goBackDirection = goBackInfo[direction]
        player.travel(direction)
        neighborRoom = player.current_room.id
        player.travel(goBackDirection)
        roomGraph[room][direction] = neighborRoom


###############################################################################
# This function finds the neighbors of a room 
# It returns a list of rooms if a key exists for the room in roomGraph
# If the key does not exist it returns None
###############################################################################
def getNeighborsRN(room):
    if not room in roomGraph:
        return None
    else:
        nbourList = []
        for direction in roomGraph[room]:
            nbourList.append(roomGraph[room][direction])
        return nbourList


###############################################################################
# This function finds the direction to walk to go to from a given room (the 
# parameter startRoom) to a neighbour room (the parameter nbourRoom)
# It returns a direction or None if the nbourRoom is not actually a neighbor of
# startRoom
###############################################################################
def getRoomDirection(startRoom,nbourRoom):
    for direction in roomGraph[startRoom]:
        if roomGraph[startRoom][direction] == nbourRoom:
            return direction


###############################################################################
# This function takes a list and moves the player in the directions 
# specified in the list
###############################################################################
def movePlayer(dirList):
    for dir in dirList:
        player.travel(dir)

###############################################################################
# This function finds the shortest path between two rooms
# It returns a list of directions to take to go from startRoom to endRoom
# It uses a modified BFS in that the roomGraph may not be completed when it is
# used, so it has to skip exploring nodes without neighbor information
###############################################################################
def getShortestPath(startRoom, endRoom):
    qq = Queue()
    qq.enqueue([startRoom])
    visited = set()
    pathFound = False
    shortestPathRN = [] # This is the shortest path in terms of room nodes
    shortestPathDir = [] # This is the shortest path in terms of n/s/e/w directions

    # This while loop finds the shortest path in terms of room nodes
    # and sets shortestPathRN
    while qq.size() > 0 and not pathFound:
        # dequeue the path (list) at the head of the queue
        current_path = qq.dequeue()
        
        # If the vertex at the end of the current path has not
        # been visited then continue building the path forward
        if current_path[-1] not in visited:
            # mark as visited
            visited.add(current_path[-1])

            # enqueue all neightbors and set pathFound and shortestPath if possible
            for next_vert in getNeighborsRN(current_path[-1]):
                new_path = list(current_path)
                new_path.append(next_vert)
                if new_path[0] == startRoom and new_path[-1] == endRoom:
                    pathFound = True
                    shortestPathRN = new_path
                if getNeighborsRN(next_vert) != None:
                    qq.enqueue(new_path)

    # This while loop creates shortestPathDir from shortestPathRN
    for ii in range(len(shortestPathRN)-1):
        direction = getRoomDirection(shortestPathRN[ii],shortestPathRN[ii+1])
        shortestPathDir.append(direction)
        
    return shortestPathDir


###############################################################################
# This function finds the traversal path
# It uses DFT to go to all the nodes
# When doubling back it uses BFS to find the sortest path from current room
# to the next room to pop off the stack in the DFT algorithm 
###############################################################################
def getTraversalPath():
    ss = Stack()
    ss.push(0)
    visited = set()

    while ss.size() > 0:
        # pop the vertex at the top of the stack
        current_vertex = ss.pop()

        if current_vertex not in visited:
            # mark as visited
            visited.add(current_vertex)
            
            # move to current_vertex from current_room
            if player.current_room.id != current_vertex:
                travel = getShortestPath(player.current_room.id, current_vertex)
                traversal_path.extend(travel)
                movePlayer(travel)
            
            #update roomGraph
            getAdjoinRoom()
            
            # push all neightbors into stack
            for next_vert in getNeighborsRN(current_vertex):
                ss.push(next_vert)
            
        

########################
# TRAVERSAL TEST
########################
getTraversalPath()
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



###########################
# UNCOMMENT TO WALK AROUND
###########################
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")



########## My test ###########################################
# Test getAdjoinRoom & get graph of test_loop_fork maze
##############################################################
# getAdjoinRoom()
# player.travel('e') # rm=3
# getAdjoinRoom()
# player.travel('e') # rm=4
# getAdjoinRoom()
# player.travel('w') # rm=3
# player.travel('w') # rm=0
# player.travel('w') # rm=7
# getAdjoinRoom() 
# player.travel('w') # rm=8
# getAdjoinRoom()
# player.travel('s') # rm=9
# getAdjoinRoom()
# player.travel('s') # rm=10
# getAdjoinRoom()                     #OK
# player.travel('e') # rm=11
# getAdjoinRoom()
# player.travel('e') # rm=6
# getAdjoinRoom()
# player.travel('n') # rm=5
# getAdjoinRoom()                     #OK
# player.travel('n') # rm=0
# player.travel('n') # rm=1
# getAdjoinRoom()
# player.travel('n') # rm=2
# getAdjoinRoom()                     #OK
# player.travel('s') # rm=1
# player.travel('w') # rm=15
# getAdjoinRoom()
# player.travel('w') # rm=16
# getAdjoinRoom()
# player.travel('n') # rm=17
# getAdjoinRoom()                     #OK
# player.travel('s') # rm=16
# player.travel('e') # rm=15
# player.travel('e') # rm=1
# player.travel('e') # rm=12
# getAdjoinRoom()
# player.travel('e') # rm=13
# getAdjoinRoom()
# player.travel('n') # rm=14
# getAdjoinRoom()                     #OK

# #Try bad direction
# player.travel('n')

# print(f'Player currently in: {player.current_room.id}')
# print(f'RoomGraph: {roomGraph}')


########## My test ###########################################
# Test getNeighborsRN 
##############################################################
# # semi populate graph
# getAdjoinRoom()
# player.travel('e') # rm=3
# getAdjoinRoom()
# print(f'Player currently in: {player.current_room.id}')
# print(f'RoomGraph: {roomGraph}')

# # test getNeighborsRN
# print(f'Neighbors of room 0: {getNeighborsRN(0)}')
# print(f'Neighbors of room 3: {getNeighborsRN(3)}')
# print(f'Neighbors of room 222: {getNeighborsRN(222)}')

########## My test ###########################################
# Test getRoomDirection 
##############################################################
# # semi populate graph
# getAdjoinRoom()
# print(f'Player currently in: {player.current_room.id}')
# print(f'RoomGraph: {roomGraph}')

# print(f'From rm0 go {getRoomDirection(0,1)} to get to rm1') 
# print(f'From rm0 go {getRoomDirection(0,3)} to get to rm3') 
# print(f'From rm0 go {getRoomDirection(0,222)} to get to rm222') 

########## My test ###########################################
# Test getShortestPath 
##############################################################
# getAdjoinRoom()
# player.travel('e') # rm=3
# getAdjoinRoom()
# player.travel('e') # rm=4
# getAdjoinRoom()
# player.travel('w') # rm=3
# player.travel('w') # rm=0
# player.travel('w') # rm=7
# getAdjoinRoom() 
# player.travel('w') # rm=8
# getAdjoinRoom()
# player.travel('s') # rm=9
# getAdjoinRoom()
# player.travel('s') # rm=10
# getAdjoinRoom()                     #OK
# player.travel('e') # rm=11
# getAdjoinRoom()
# player.travel('e') # rm=6
# getAdjoinRoom()

# player.travel('n') # rm=5
# getAdjoinRoom()                     #OK

# print(f'Player currently in: {player.current_room.id}')
# print(f'RoomGraph: {roomGraph}')

# print(f'Shortest path from 0 to 4: {getShortestPath(0,4)}')
# print(f'Shortest path from 6 to 0: {getShortestPath(6,0)}')
# print(f'Shortest path from 5 to 5: {getShortestPath(5,5)}')
# print(f'Shortest path from 0 to 0: {getShortestPath(0,0)}')
# print(f'Shortest path from 8 to 8: {getShortestPath(8,8)}')
# print(f'Shortest path from 3 to 3: {getShortestPath(3,3)}')
# print(f'Shortest path from 4 to 4: {getShortestPath(4,4)}')


########## My test ###########################################
# Test getShortestPath 
##############################################################
# getAdjoinRoom()

# print(f'Player currently in: {player.current_room.id}')
# print(f'RoomGraph: {roomGraph}')

# print(f'Shortest path from 0 to 3: {getShortestPath(0,3)}')



########## My test ###########################################
# Test movePlayer
##############################################################
# getAdjoinRoom()
# player.travel('e') # rm=3
# getAdjoinRoom()
# player.travel('e') # rm=4
# getAdjoinRoom()
# player.travel('w') # rm=3
# player.travel('w') # rm=0
# player.travel('w') # rm=7
# getAdjoinRoom() 
# player.travel('w') # rm=8
# getAdjoinRoom()
# player.travel('s') # rm=9
# getAdjoinRoom()
# player.travel('s') # rm=10
# getAdjoinRoom()                     #OK
# player.travel('e') # rm=11
# getAdjoinRoom()
# player.travel('e') # rm=6
# getAdjoinRoom()
# player.travel('n')
# player.travel('n')

# print(f'RoomGraph: {roomGraph}')
# print(f'Player currently in: {player.current_room.id}')

# shrtPath_0_6 = getShortestPath(0,6)
# print(f'Shortest path from 0 to 6: {shrtPath_0_6}')
# print(f'Travelling from 0 to 6')
# movePlayer(shrtPath_0_6)
# print(f'Player currently in: {player.current_room.id}')








