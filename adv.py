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
        exits = self.get_exits(starting_vertex)
        for exit in exits:
            print(exits[exit])
            path = [{exit:exits[exit]}]
            print('this is the path', path)
            q.enqueue(path)
        visited = set()
        while q.size() > 0:
            path = q.dequeue()
            v = path[-1]
            # if v not in visited:
            #     visited.add(v)

            print('this is v', v)
            for k, d in v.items():
                dir = k
                room = d
            print('room now:', room)
            print('path', path)
            if room == '?':
                dirback = []
                print('\npath before:', path)

                for d in path:
                    for k in d:
                        dirback.append(k)
                print('DIRECTIONS BACK:', dirback)
                return dirback

            exits = self.get_exits(room)
            for exit in exits:
                newpath = list(path)
                newpath.append({exit:exits[exit]})
                q.enqueue(newpath)



        # q = Queue()
        # cur = starting_vertex
        # for dir, room in self.get_exits(cur).items():
        #     q.enqueue([{dir:room}])
        #     print('DIR:', dir, 'Rooms:', room)
        # # for exit in exits:
        # #     #print(exit)
        # path = []
        #
        # while q.size() > 0:
        #     v = q.dequeue()
        #     print('v', v)
        #     for key, val in v[-1].items():
        #         dir = key
        #         room = val
        #
        #     print('dir:', dir, 'val', val)
        #     path.append(v)
        #     print('path', path)
        #     # if room == '?':
        #     #     return path
        #     print('room:', room)
        #     print('outside:', self.get_exits(room))
        #
        #     for dir, rm in self.get_exits(val).items():
        #         #print('dir, room', dir, rm)
        #         if rm == '?':
        #             dirback = []
        #             print('\npath before:', path)
        #
        #             for d in path:
        #                 for k in d:
        #                     dirback.append(k)
        #             print('DIRECTIONS BACK:', dirback)
        #             return dirback
        #         newpath = path
        #         newpath.append({dir:rm})
        #         q.enqueue(newpath)

# Fill this out with directions to walk
###
#initialize graph
g = Graph()
cur = player.current_room
g.add_vertex(cur.id)
g.add_exits(cur.id, cur.get_exits())
move = 'w'
traversal_path = []

while len(g.vertices) < 500:
    print('\n\n----graph size :', len(g.vertices), '\n\n')
    while move != None:
        prev_room = player.current_room.id
        print('\ndirection moved:',move)

        player.travel(move)
        traversal_path.append(move)
        print(traversal_path)
        #link previous room
        cur = player.current_room
        g.vertices[prev_room][move] = cur.id

        if cur.id not in g.vertices:
            g.add_vertex(cur.id)
            g.add_exits(cur.id, cur.get_exits())
        #add link to previous room
        if move =='n':
            g.vertices[cur.id]['s'] = prev_room
        elif move == 's':
            g.vertices[cur.id]['n'] = prev_room
        elif move == 'e':
            g.vertices[cur.id]['w'] = prev_room
        elif move == 'w':
            g.vertices[cur.id]['e'] = prev_room
        #pick a direction to move in
        print('\n\n----graph size :', len(g.vertices), '\n\n')
        poss_moves = []
        for x in g.vertices[cur.id]:
            if g.vertices[cur.id][x] == '?':
                poss_moves.append(x)
        print('possible moves', poss_moves)
        if len(poss_moves) == 0:
             move = None
             print('room', cur.id, 'exits:', g.vertices[cur.id])
        else:

            move = poss_moves[0]
    print('time to implement!')
    goback = g.bfs(player.current_room.id)
    print(goback)
    for step in goback:
        player.travel(step)
        traversal_path.append(step)
    move = goback[-1]
    # if 'n' in g.vertices[cur.id]:
    #     if g.vertices[cur.id]['n'] == '?':
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
