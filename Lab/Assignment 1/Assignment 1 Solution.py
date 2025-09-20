#Part1
import heapq

class Node:
    def __init__(self, row, col, gCost=0, hCost=0, parent=None, action=''):
        self.row = row
        self.col = col
        self.gCost = gCost
        self.hCost = hCost
        self.fCost = gCost + hCost
        self.parent = parent
        self.action = action

    def __lt__(self, other):
        if self.fCost == other.fCost:
            return self.hCost < other.hCost
        return self.fCost < other.fCost

def calculateManhattanDistance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def aStarMazeSolver(maze, start, goal):
    n = len(maze)
    m = len(maze[0])
    directions = [(-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R')]
    priorityQueue = []
    visited = []
    for i in range(n):
        row = []
        for j in range(m):
            row.append(False)
        visited.append(row)
    startH = calculateManhattanDistance(start[0], start[1], goal[0], goal[1])
    startNode = Node(start[0], start[1], 0, startH)
    heapq.heappush(priorityQueue, startNode)
    while priorityQueue:
        current = heapq.heappop(priorityQueue)
        if (current.row, current.col) == goal:
            path = []
            totalCost = current.gCost
            while current.parent is not None:
                path.append(current.action)
                current = current.parent
            return totalCost, ''.join(reversed(path))
        if visited[current.row][current.col]:
            continue
        visited[current.row][current.col] = True
        for dx, dy, action in directions:
            nx = current.row + dx
            ny = current.col + dy
            if 0 <= nx < n and 0 <= ny < m:
                if maze[nx][ny] == '0' and not visited[nx][ny]:
                    g = current.gCost + 1
                    h = calculateManhattanDistance(nx, ny, goal[0], goal[1])
                    neighborNode = Node(nx, ny, g, h, current, action)
                    heapq.heappush(priorityQueue, neighborNode)
    return -1, ''

# driver code
lines = []
with open('input.txt') as f:
    for line in f:
        line = line.strip()
        if line != '':
            lines.append(line)

n, m = map(int, lines[0].split())
start = tuple(map(int, lines[1].split()))
goal = tuple(map(int, lines[2].split()))
maze = []
for i in range(3, len(lines)):
    line = lines[i].replace(' ', '')
    row = []
    for ch in line:
        row.append(ch)
    maze.append(row)

cost, path = aStarMazeSolver(maze, start, goal)

with open('output.txt', 'w') as f:
    if cost == -1:
        f.write("No path found.")
    else:
        f.write(path + '\n')
        f.write(f"Total steps: {cost}")







#Part2
# import heapq

# def aStar(start, goal):
#     priorityQueue = [(heuristics[start], 0, start)]
#     gCost = {node: float('inf') for node in range(1, n + 1)}
#     gCost[start] = 0
#     visited = set()

#     while priorityQueue:
#         f_current, gCurrent, current = heapq.heappop(priorityQueue)
#         if current == goal:
#             return gCurrent
#         if current in visited:
#             continue
#         visited.add(current)
#         for neighbor in graph.get(current, []):
#             g = gCurrent + 1
#             if g < gCost[neighbor]:
#                 gCost[neighbor] = g
#                 fNeighbor = g + heuristics[neighbor]
#                 heapq.heappush(priorityQueue, (fNeighbor, g, neighbor))
#     return float('inf')


# with open('input2.txt', 'r') as f:
#     lines = []
#     for line in f:
#         line = line.strip()
#         if line != '':
#             lines.append(line)
            
# n, m = map(int, lines[0].split())
# a, b = map(int, lines[1].split())
# heuristics = {}
# for i in range(n):
#     x, y = map(int, lines[2 + i].split())
#     heuristics[x] = y
# graph = {}
# for i in range(m):
#     u, v = map(int, lines[2 + n + i].split())
#     if u not in graph:
#         graph[u] = []
#     if v not in graph:
#         graph[v] = []
#     graph[u].append(v)
#     graph[v].append(u)

# inadmissibleNodes = []
# for node in range(1, n + 1):
#     trueCost = aStar(node, b)
#     if heuristics[node] > trueCost:
#         inadmissibleNodes.append(node)

# with open('output2.txt', 'w') as fOut:
#     if inadmissibleNodes:
#         fOut.write('0\n')
#         fOut.write("Here nodes " + ', '.join(map(str, inadmissibleNodes)) + " are inadmissible.")
#     else:
#         fOut.write('1')