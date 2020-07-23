# SlidePuzzlePathfinder
Slide Puzzle Game with Pathfinder Algorithm Solver

# Technologies
### Language Version
    Python 3.7.7
### Required Packages
    Pygame 1.9.6
### Required Modules 
    Random
    sys
    enum
    time
    
# Getting Started
### Installation
    Confirm that all Technologies are installed with the requested version
    Newer/Older versions of Python and Pygame may be compatible but are not guarenteed to work

### Run
    run py_slider.py
    
### Gameplay
    Upon starting the game the board will be shuffled
    Pressing esc or Clicking the 'X' in the top right corner will terminate the game
    Clicking a tile adjacent to the 'Blank' Tile will swap its position with the blank tile
    The Arrow Keys and W-A-S-D can also be used to move the tiles on the board
    The game is 'Won' when the board reaches the following state:
    
                        1         2         3
                        
                        4         5         6
                        
                        7         8        
                        
    Reset - Resets the board to the 'New Game' State
    New Game - Shuffles the board to a 'New' starting state
    Solve - Uses the A* Pathfinding algorithm to find the most optimal solution for the puzzle
    
### Game Modification
    Within py_slide.py there are multiple Constants to modify the game
    
    SOLUTION_METHOD - Determines the pathfinding algorithm that will be used to solve the puzzle
    TEST_MODE - Used when testing functions to prevent failures from unloaded graphics
    BOARD_WIDTH - Determines the number of horizontal tiles 
    BOARD_HEIGHT - Determines the number of vertical tiles
    WINDOW_WIDTH - Determines the width of the game window
    WINDOW_HEIGHT - Determines the height of the game window
    ANTI_ALIASING - Activates ANTI_ALIASING for game text - True = Enabled
    FPS - Sets the Maximum framerate of the game graphics
    
    Many other modifications can be made by modifying other constants 
    
### Testing
    Unit tests are proided to test all non graphical functionality. 
    Solution tests are tested based on their ability to solve a randome puzzle There are no tests currently that handle the specific functions within each test method
    
    pytest is used as the test harness:
    *pytest solver_logic_unit_tests.py* can be used to test solver logic
        These tests check the solvers ability to solve a random puzzle
        These tests also stress test the solver by testing multiple tests side by side
    
    *pytest board_logic_unit_tests.py* can be used to test the board logic
        These tests check the functionality of all non graphical board logic functions
        
    -r A can be used to show the output of all tests (Pass/Fail/Skipped)
    -s can be used to show test results in real time
    
    
    
    



