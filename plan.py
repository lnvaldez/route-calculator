'''
1. Create a Pygame window
2. Generate a grid of defined size within the grid
3. Grid matrix is user defined, i.e. 10x10, 10x12
4. Allow user to modify color of each rect in grid by toggling coloring with keyboard
    White square = free route
    Gray square = building \ NO PASS
    Blue square = body of water / NO PASS
    Yellow square = construction /NO PASS
    White square w/ red circle = STARTING POINT
    White square w/ green circle = END POINT
5. User can toggle which screen to look at 
3 screens:
1. Explanation
2. Design
3. Solved state (shortest route)
    If no solved state available
        return NO SOLVE
'''