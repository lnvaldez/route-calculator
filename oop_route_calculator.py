import curses
import numpy as np
import heapq

class ANSI:
    RED_CLR = '\x1b[31m'
    GREEN_CLR = '\x1b[32m'
    BLUE_CLR = '\x1b[34m'
    YELLOW_CLR = '\x1b[33m'
    LIGHT_GRAY_BG = '\x1b[47m'
    END_CLR = '\033[0m'

# Colors for curses
class Color:
    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = 4
    CYAN = 5
    MAGENTA = 6
    WHITE = 7

class Map:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = np.array([["□" for _ in range(cols)] for _ in range(rows)], dtype=str)
        self.start = None
        self.end = None

    def draw_grid(self, stdscr, cursor_x, cursor_y):
        for y in range(self.rows):
            for x in range(self.cols):
                if y == cursor_y and x == cursor_x:
                    stdscr.addstr(y, x * 2, self.grid[y][x], curses.A_REVERSE)
                else:
                    ch = self.grid[y][x]
                    color = curses.color_pair(0)
                    if ch == '☰':
                        color = curses.color_pair(Color.RED)
                    elif ch == '○':
                        color = curses.color_pair(Color.BLUE)
                    elif ch == '△':
                        color = curses.color_pair(Color.YELLOW)
                    elif ch == '■':
                        color = curses.color_pair(Color.GREEN)
                    elif ch == '⧇':
                        color = curses.color_pair(Color.CYAN)
                    stdscr.addstr(y, x * 2, ch, color)

    def set_cell(self, y, x, value):
        self.grid[y][x] = value

class Route:
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def a_star_search(grid, start, end):
        rows, cols = grid.shape
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: Route.heuristic(start, end)}

        while open_set:
            current = heapq.heappop(open_set)[1]

            if current == end:
                Route.reconstruct_path(grid, came_from, current)
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
                        f_score[neighbor] = tentative_g_score + Route.heuristic(neighbor, end)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return False

    def reconstruct_path(grid, came_from, current):
        while current in came_from:
            current = came_from[current]
            if grid[current[0]][current[1]] not in ('⧇'):
                grid[current[0]][current[1]] = '■'

RED = ANSI.RED_CLR
GREEN = ANSI.GREEN_CLR
BLUE = ANSI.BLUE_CLR
YELLOW = ANSI.YELLOW_CLR
LIGHT_GRAY_BG = ANSI.LIGHT_GRAY_BG
END = ANSI.END_CLR

ascii_art = '''
 _______  __   __  _______  _______  ______    ___   _______  ___     
|       ||  | |  ||       ||       ||    _ |  |   | |   _   ||   |    
|_     _||  | |  ||_     _||   _   ||   | ||  |   | |  |_|  ||   |    
  |   |  |  |_|  |  |   |  |  | |  ||   |_||_ |   | |       ||   |    
  |   |  |       |  |   |  |  |_|  ||    __  ||   | |       ||   |___ 
  |   |  |       |  |   |  |       ||   |  | ||   | |   _   ||       |
  |___|  |_______|  |___|  |_______||___|  |_||___| |__| |__||_______|
'''

print(f"""
{YELLOW}{ascii_art}{END}
{YELLOW}{'-`/.' * 20}{END}
{RED}Start and End Points:{END}
Press 'S' to add a start point, and 'E' to add an end point.
{GREEN}Obstacles:{END}
Press 'B' to add buildings, 'W' for water, and 'C' for construction sites.
{BLUE}Path, Reset and Quit:{END}
Press 'R' to overwrite to a path, 'I' to reset the grid and 'Q' twice to exit.
{YELLOW}{'-`/.' * 20}{END}""")

rows = int(input("Enter amount of rows: "))
cols = int(input("Enter amount of columns: "))

def run(stdscr):
    curses.curs_set(0)
    curses.start_color()
    
    curses.init_pair(Color.RED, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(Color.GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(Color.BLUE, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(Color.YELLOW, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(Color.CYAN, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(Color.MAGENTA, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(Color.WHITE, curses.COLOR_WHITE, curses.COLOR_BLACK)

    stdscr.clear()

    map_instance = Map(rows, cols)
    cursor_x = 0
    cursor_y = 0

    while True:
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        
        if max_y < rows or max_x < cols * 2:
            stdscr.addstr(0, 0, "Resize the window.", curses.A_BOLD)
        else:
            map_instance.draw_grid(stdscr, cursor_x, cursor_y)

        key = stdscr.getch()

        if key == curses.KEY_UP and cursor_y > 0:
            cursor_y -= 1
        elif key == curses.KEY_DOWN and cursor_y < rows - 1:
            cursor_y += 1
        elif key == curses.KEY_LEFT and cursor_x > 0:
            cursor_x -= 1
        elif key == curses.KEY_RIGHT and cursor_x < cols - 1:
            cursor_x += 1
        elif key == ord('1'):  
            map_instance.set_cell(cursor_y, cursor_x, '⧇')
            if map_instance.start:
                map_instance.set_cell(map_instance.start[0], map_instance.start[1], '□')
            map_instance.start = (cursor_y, cursor_x)
        elif key == ord('2'):  
            map_instance.set_cell(cursor_y, cursor_x, '⧇')
            if map_instance.end:
                map_instance.set_cell(map_instance.end[0], map_instance.end[1], '□')
            map_instance.end = (cursor_y, cursor_x)
        elif key == ord('3'):
            map_instance.set_cell(cursor_y, cursor_x, '□')
        elif key == ord('4'):  
            map_instance.set_cell(cursor_y, cursor_x, '☰')
        elif key == ord('5'): 
            map_instance.set_cell(cursor_y, cursor_x, '○')
        elif key == ord('6'):  
            map_instance.set_cell(cursor_y, cursor_x, '△')
        elif key == ord('q'):  
            break
        elif key == ord('a'):  
            if map_instance.start and map_instance.end:
                Route.a_star_search(map_instance.grid, map_instance.start, map_instance.end)
        elif key == ord('0'):
            for i in range(0, rows):
                for j in range(0, cols):
                    map_instance.set_cell(i, j, '□')

    stdscr.clear()
    for y in range(rows):
        for x in range(cols):
            ch = map_instance.grid[y][x]
            color = curses.color_pair(0)
            if ch == '☰':
                color = curses.color_pair(Color.RED)
            elif ch == '○':
                color = curses.color_pair(Color.BLUE)
            elif ch == '△':
                color = curses.color_pair(Color.YELLOW)
            elif ch == '■':
                color = curses.color_pair(Color.GREEN)
            elif ch == '⧇':
                color = curses.color_pair(Color.CYAN)
            stdscr.addstr(y, x * 2, ch, color)
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(run)
