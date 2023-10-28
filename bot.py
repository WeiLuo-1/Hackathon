import heapq
import socket

class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f


def find_entries(maze):
    entrance = None
    exit = None
    for i, row in enumerate(maze):
        for j, spot in enumerate(row):
            if spot == 3:  # 3 represents the entrance
                entrance = (i, j)
            elif spot == 2:  # 2 represents the exit
                exit = (i, j)

    if entrance is None or exit is None:
        raise ValueError("Maze must have an entrance (3) and an exit (2)")
    return entrance, exit


def astar(maze):
    start, end = find_entries(maze)

    start_node = Node(None, start)
    end_node = Node(None, end)

    open_list = []
    closed_list = []

    heapq.heapify(open_list)
    heapq.heappush(open_list, start_node)

    outer_iterations = 0
    max_iterations = (len(maze) // 2) ** 10

    while open_list:
        outer_iterations += 1

        if outer_iterations > max_iterations:
            # Establish a way to exit the loop
            print("giving up on pathfinding too many iterations")
            return return_path(current_node)

        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        if current_node == end_node:
            return return_path(current_node)

        children = []

        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:

            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            within_range_conditions = [
                node_position[0] > (len(maze) - 1),
                node_position[0] < 0,
                node_position[1] > (len(maze[len(maze) - 1]) - 1),
                node_position[1] < 0,
            ]

            if any(within_range_conditions):
                continue

            if maze[node_position[0]][node_position[1]] == 1:
                continue

            new_node = Node(current_node, node_position)

            children.append(new_node)

        for child in children:
            if child in closed_list:
                continue

            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                (child.position[1] - end_node.position[1]) ** 2
            )
            child.f = child.g + child.h

            if add_to_open(open_list, child):
                heapq.heappush(open_list, child)

    return None


def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path


def add_to_open(open_list, child):
    for open_node in open_list:
        if child == open_node and child.g > open_node.g:
            return False
    return True


def main():
    maze: list[list[int]] = []

    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('localhost', 42000))

    clientsocket.send('get_state\n'.encode('ascii'))
    clientsocket.settimeout(10)
    state = clientsocket.recv(1000000)
    response = state.decode('ascii')
    print(response)

    playerx, playery, columns, mazetext = response.split()
    playerx = int(playerx)
    playery = int(playery)
    columns = int(columns)

    row = 0
    while len(mazetext) > 0:
        maze.append([])
        for col in range(columns):
            c = mazetext[0]
            mazetext = mazetext[1:]
            maze[row].append(int(c))

        row += 1
    
    for row in maze:
        print(row)

    path = astar(maze)
    print(path)

    commands: list[str] = []

    for i in range(len(path) - 1):
        currentposition = path[i]
        nextposition = path[i+1]
        dx = nextposition[1] - currentposition[1]
        dy = nextposition[0] - currentposition[0]
        if dx == -1:
            commands.append('move_left\n')
        if dx == 1:
            commands.append('move_right\n')
        if dy == -1:
            commands.append('move_up\n')
        if dy == 1:
            commands.append('move_down\n')
        
    print(commands)

    for command in commands:
        clientsocket.send(command.encode('ascii'))

if __name__ == "__main__":
    main()
