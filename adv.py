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
        self.vertices[vertex_id] = set()

    def add_exits(self, room, exits):
        """
        Add exits to room_id:
        input: room = 0 exits = {'n':'?','s':'?','e':'?','w':'?'}
        output:  0:{'n':'?','s':'?','e':'?','w':'?'}
        """
        if room in self.vertices:
            self.vertices[room] = exits

    def get_exits(self, vertex_id):
        """
        return all room exit information.
        """
        if vertex_id not in self.vertices:
            return None
        return self.vertices[vertex_id]

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        q = Queue()
        path = [starting_vertex]
        q.enqueue(path)
        visited = set()
        while q.size() > 0:
            path = q.dequeue()
            v = path[-1]
            if v not in visited:
                visited.add(v)
                if v == destination_vertex:
                    return path

                for next_vert in self.get_neighbors(v):
                    newpath = list(path)
                    newpath.append(next_vert)
                    q.enqueue(newpath)

# Fill this out with directions to walk
###
#initialize graph
g = Graph()
cur = player.current_room
g.add_vertex(cur.id)
g.add_exits(cur.id, cur.get_exits())
move = 'n'
traversal_path = [move]
while move != None:
    prev_room = player.current_room.id
    player.travel(move)
    #link previous room
    cur = player.current_room
    g.vertices[prev_room][move] = cur.id

    if cur.id not in g.vertices:
        g.add_vertex(cur.id)
        g.add_exits(cur.id, cur.get_exits())
    #add link to previous room
    if move = 'n':
        g.vertices[cur.id]['s'] = prev_room
    elif move = 's':
        g.vertices[cur.id]['n'] = prev_room
    elif move = 'e':
        g.vertices[cur.id]['w'] = prev_room
    elif move = 'w':
        g.vertices[cur.id]['e'] = prev_room
    #pick a direction to move in
    for exit in g.vertices[cur.id]:
        if exit = '?'
###
# traversal_path = ['n', 'n']
traversal_path = []



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
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
