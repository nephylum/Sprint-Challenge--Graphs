from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

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
####
class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = {}

    def add_exits(self, room, exits):
        """
        Add exits to room_id:
        input: room = 0 exits = {'n':'?','s':'?','e':'?','w':'?'}
        output:  0:{'n':'?','s':'?','e':'?','w':'?'}
        """
        if room in self.vertices:
            for exit in exits:
                self.vertices[room][exit] = '?'

    def get_exits(self, vertex_id):
        """
        return all room exit information.
        """
        if vertex_id not in self.vertices:
            return None
        return self.vertices[vertex_id]

    def bfs(self, starting_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breadth-first order.
        """
        q = Queue()
        path = []
        cur_room = starting_vertex
        for next_vert in self.get_exits(cur_room):
            newpath=list(path)
            newpath.append({next_vert: cur_room})
            q.enqueue(newpath)
        print('room:', cur_room, 'exits:', self.get_exits(cur_room), 'path', newpath,'\n')
        #define visited

        while q.size() > 0:
            path = q.dequeue()
            v = path[-1]


            for key in v:
                direction = key
                room = v[key]

            cur_room = g.vertices[room][direction]
            print('room:', cur_room, 'exits:', self.get_exits(cur_room), 'path', path,'\n')

            for dirs in g.vertices[cur_room]:
                newpath = list(path)

                print("direction", dirs)
                if g.vertices[cur_room][dirs] == '?':
                    pathback = []
                    print('\nPath before cleaining:', newpath)
                    for steps in newpath:
                        for directions in steps:
                            pathback.append(directions)
                    return pathback
                #to prevent back-tracking (looping)
                visited = set()
                for steps in newpath:
                    for ds in steps:
                        visited.add(steps[ds])

                if g.vertices[cur_room][dirs] not in visited:
                    visited.add(g.vertices[cur_room][dirs])
                    newpath.append({dirs: cur_room})
                    q.enqueue(newpath)



# Fill this out with directions to walk
###
#initialize graph

g = Graph()
traversal_path = []
move = None
prev_room = None
while len(g.vertices) < 500:


    #move loop
    while move != 'GOBACK':

        cur_room = player.current_room.id
        exits = player.current_room.get_exits()

        #update graph
        print('room id:', player.current_room.id)
        if player.current_room.id not in g.vertices:
            g.add_vertex(player.current_room.id)
            g.add_exits(player.current_room.id, exits)
            print("\n\n-------Graph Size -----=:", len(g.vertices))
        #update exit for previous room in graph
        if move != None:
            if move == 'n':
                g.vertices[prev_room]['n'] = player.current_room.id
                g.vertices[player.current_room.id]['s'] = prev_room
            if move == 's':
                g.vertices[prev_room]['s'] = player.current_room.id
                g.vertices[player.current_room.id]['n'] = prev_room
            if move == 'w':
                g.vertices[prev_room]['w'] = player.current_room.id
                g.vertices[player.current_room.id]['e'] = prev_room
            if move == 'e':
                g.vertices[prev_room]['e'] = player.current_room.id
                g.vertices[player.current_room.id]['w'] = prev_room
            pass
        else:
            #if room not in graph add room to graph
            #if exit not updated. update exit
            pass

        #find next exit
        known_exits = g.get_exits(player.current_room.id)
        to_move = []
        for exit in known_exits:
            print('exit', exit, 'exits', exits)
            if g.vertices[player.current_room.id][exit] == '?':
                to_move.append(exit)
                break
        if len(to_move) == 0:
            move = 'GOBACK'
            print("\nCAN'T MOVE!\n")
        else:
            move = to_move[0]

        prev_room = player.current_room.id
        if move != 'GOBACK' and move != None:
            print(move)
            player.travel(move)
            traversal_path.append(move)








# g = Graph()
# cur = player.current_room
# g.add_vertex(cur.id)
# g.add_exits(cur.id, cur.get_exits())
# move = 'w'
# traversal_path = []
#
# while len(g.vertices) < 500:
#     print('\n\n----graph size :', len(g.vertices), '\n\n')
#     while move != None:
#         prev_room = player.current_room.id
#         print('\ndirection moved:',move)
#
#         player.travel(move)
#         traversal_path.append(move)
#         print(traversal_path)
#         #link previous room
#         cur = player.current_room
#         print('current room:',cur.id, 'previous room', prev_room,'move',move)
#         g.vertices[prev_room][move] = cur.id
#
#         if cur.id not in g.vertices:
#             g.add_vertex(cur.id)
#             g.add_exits(cur.id, cur.get_exits())





        #add link to previous room
        # if move =='n':
        #     if g.vertices[cur.id]['s'] == '?':
        #         g.vertices[cur.id]['s'] = prev_room
        # elif move == 's':
        #     if g.vertices[cur.id]['n'] == '?':
        #         g.vertices[cur.id]['n'] = prev_room
        # elif move == 'e':
        #     if g.vertices[cur.id]['w'] == '?':
        #         g.vertices[cur.id]['w'] = prev_room
        # elif move == 'w':
        #     if g.vertices[cur.id]['e'] == '?':
    #     #         g.vertices[cur.id]['e'] = prev_room
    #     #pick a direction to move in
    #     print('\n\n----graph size :', len(g.vertices), '\n\n')
    #
    #     poss_moves = []
    #     for x in g.vertices[cur.id]:
    #         if g.vertices[cur.id][x] == '?':
    #             poss_moves.append(x)
    #     print('possible moves', poss_moves)
    #     if len(poss_moves) == 0:
    #          move = None
    #          print('room', cur.id, 'exits:', g.get_exits(cur.id))
    #     else:
    #
    #         move = poss_moves[0]
    #
    #
    print('time to implement!')
    print('Room before bfs', player.current_room.id)
    goback = g.bfs(player.current_room.id)
    print('goback', goback)
    print('size of graph:', len(g.vertices))
    if len(goback) >= 1:

        for step in goback:
            print('step', step)
            player.travel(step)
            traversal_path.append(step)
            move = step
    #
    # move = goback[-1]
    # print('goback move!::', move)
    # # if 'n' in g.vertices[cur.id]:
    # #     if g.vertices[cur.id]['n'] == '?':
    #         move = 'n'
    # if 's' in g.vertices[cur.id]:
    #     if g.vertices[cur.id]['s'] == '?':
    #         move = 's'
    # if 'e' in g.vertices[cur.id]:
    #     if g.vertices[cur.id]['e'] == '?':
    #         move = 'e'
    # if 'w' in g.vertices[cur.id]:
    #     if g.vertices[cur.id]['s'] == '?':
    #         move = 's'
    # elif ((g.vertices[cur.id]['n'] != '?') and (g.vertices[cur.id]['s'] != '?')
    #     and (g.vertices[cur.id]['e'] != '?') and (g.vertices[cur.id]['w'] != '?')):
    #      move = None

###




# TRAVERSAL TEST - DO NOT MODIFY
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



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
