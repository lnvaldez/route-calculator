import numpy as np
import heapq

class Color:
    RED_CLR = '\x1b[31m'
    GREEN_CLR = '\x1b[32m'
    END_CLR = '\033[0m'

def create_grid(rows, cols):
    return np.array([[f"□" for _ in range(cols)] for _ in range(rows)])

def print_grid(grid):
    print('->'*30)
    print("  ", end="")  # Add space for alignment
    for i in range(cols):
        print(f"{RED}{i}{END}", end=" ")

    print(' ')

    for count, row in enumerate(grid):
        print(f"{RED}{count}{END}", f"{GREEN}{' '.join(row)}{END}")

def add_start_end():
    print('->'*30)
    startX, startY = [int(x) for x in input("Add start coordinates: \n").split(',')]
    grid[startX][startY] = '⧇'
    endX, endY = [int(x) for x in input("Add end coordinates: \n").split(',')]
    grid[endX][endY] = '⧇'
    return (startX, startY), (endX, endY)

def add_obstacles():
    print('->'*30)
    while True:
        print("Add obstacles (format: '1,1,b 2,2,w 3,3,c'): ")
        obstacles = input()
        coords = [x.split(',') for x in obstacles.split()]

        for x, y, obstacle_type in coords:
            a, b = int(x), int(y)
            if 0 <= a < row and 0 <= b < cols:
                if obstacle_type == 'b':
                    grid[a][b] = '☰'
                elif obstacle_type == 'w':
                    grid[a][b] = '○'
                elif obstacle_type == 'c':
                    grid[a][b] = '△'
                else:
                    print(f"Unknown obstacle type: {obstacle_type}")

        print_grid(grid)

        user_input = input("Continue(y/n): ")
        if user_input.lower() != 'y':
            break

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(grid, start, end):
    rows, cols = grid.shape
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == end:
            reconstruct_path(came_from, current)
            return True

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if grid[neighbor[0]][neighbor[1]] == '☰':
                    continue 
                elif grid[neighbor[0]][neighbor[1]] == '○':
                    tentative_g_score = g_score[current] + 5  
                elif grid[neighbor[0]][neighbor[1]] == '△':
                    tentative_g_score = g_score[current] + 3
                else:
                    tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return False

def reconstruct_path(came_from, current):
    while current in came_from:
        current = came_from[current]
        if grid[current[0]][current[1]] not in ('⧇', '⧇'):
            grid[current[0]][current[1]] = '■'
    print_grid(grid)

RED = Color.RED_CLR
GREEN = Color.GREEN_CLR
END = Color.END_CLR

row = int(input("Enter amount of rows: "))
cols = int(input("Enter amount of columns: "))

grid = create_grid(rows=row, cols=cols)
print_grid(grid)
start, end = add_start_end()
add_obstacles()

if a_star_search(grid, start, end):
    print("Path found and marked on the grid.")
else:
    print("No path found.")

print_grid(grid)
