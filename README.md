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
    
    BOARD_WIDTH - Determines the number of horizontal tiles 
    BOARD_HEIGHT - Determines the number of vertical tiles
    WINDOW_WIDTH - Determines the width of the game window
    WINDOW_HEIGHT - Determines the height of the game window
    ANTI_ALIASING - Activates ANTI_ALIASING for game text - True = Enabled
    FPS - Sets the Maximum framerate of the game graphics
    
    Many other modifications can be made by modifying other constants 
    
    
    



