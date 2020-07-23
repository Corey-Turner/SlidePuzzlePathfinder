import pygame, sys, random, enum, time,threading
from pygame.locals import *

# Solution Constants
SOLUTION_METHOD = 1         # Determines the solution that will be used to solve the puzzle
                            # 0 = Shortest Path First
                            # 1 = A Star Method

# Test Constant
TEST_MODE = False      # Used in Unit tests to prevent test from failing due to graphics not being loaded

# Board Size Constants
BOARD_WIDTH = 3      # Determines the number of horizontal tiles
BOARD_HEIGHT = 3     # Determines the number of vertical tiles

# Color Constants
# RGB Values for display Colors
#          R    G    B
BLACK =  (  0,   0,   0)
WHITE =  (255, 255, 255)
TEAL =   (115, 198, 182)
PURPLE = (108,  52, 131)
MAROON = (123,  36,  28)

# Game object Constants
TILE_COLOR = MAROON
BLANK_TILE_COLOR = PURPLE
BORDER_COLOR = TEAL
BUTTON_COLOR = WHITE
BUTTON_TEXT_COLOR = BLACK
TILE_SIZE = 80               # Game tile Side length

# Text Constants
TEXT_COLOR = WHITE
MESSAGE_COLOR = WHITE
BACK_COLOR = PURPLE
BASIC_FONT_SIZE = 20

# Game Window Constants
WINDOW_WIDTH = 640          # Width of the game window
WINDOW_HEIGHT = 480         # Height of the game window
ANTI_ALIASING = True        # Enables Anti Aliasing : True = Enabled
MESSAGE_Y_LOC = 5           # Y Location of the game status message
MESSAGE_X_LOC = 5           # X Location of the game status message
FPS = 60                    # Graphical Refresh Rate

# Margin For Border constraining game tiles
X_MARGIN = int((WINDOW_WIDTH - (TILE_SIZE * BOARD_WIDTH + (BOARD_WIDTH - 1))) / 2)
Y_MARGIN = int((WINDOW_HEIGHT - (TILE_SIZE * BOARD_HEIGHT + (BOARD_HEIGHT - 1))) / 2)

# Global Variables
FPS_CLOCK = None            # Used for timing display refresh
DISPLAY_SURFACE = None      # Surface that contains all game graphics
BASIC_FONT = None           # Text Font used for all game text
RESET_GAME_SURFACE = None   # Surface that contains the 'Reset' Button
RESET_GAME_RECT = None      # Rectangle that constrains the 'Reset' Button
NEW_GAME_SURFACE = None     # Surface that contains the 'New Game' Button
NEW_GAME_RECT = None        # Rectangle that constrains the 'New Game' Button
SOLVE_GAME_SURFACE = None   # Surface that contains the 'Solve' Button
SOLVE_GAME_RECT = None      # Rectangle that constrains the 'Solve' Button
SOLUTION_NODE = None
SOLVER_COMPLETE = None
BOARDS_ANALYZED = 0
TERMINATED = False

# Enumeration to map player move directions
# UP represents a Tile moving UP into the empty square
# a move should be set to UNCHANGED when no move has been selected
class PlayerMoves(enum.Enum):
    UNCHANGED = None
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


# Checks if the player closes the window or presses esc
# terminates game on user quit
def check_for_quit():
    global TERMINATED
    # Exits the game and closes the game console
    def terminate_game():
        pygame.quit()
        sys.exit()

    if TEST_MODE:
        return
    for event in pygame.event.get(QUIT):
        TERMINATED = True
        time.sleep(2)
        terminate_game()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            TERMINATED = True
            time.sleep(2)
            terminate_game()
        pygame.event.post(event)


# Creates Surface object and TextBox rectangle objects for Text
# Returns (display) surface, (rect) textbox
def create_text(text, fore_color, back_color, top, left):
    global BASIC_FONT

    text_surface = BASIC_FONT.render(text, ANTI_ALIASING, fore_color, back_color)
    text_box = text_surface.get_rect()
    text_box.topleft = (top, left)
    return text_surface, text_box


# Updates the DISPLAY_SURFACE with the given tile information
# adj_x and adj_y offset the position of the tile based on the provided value
# the value provided for text will be drawn onto the tile
def draw_tile(tile_x, tile_y, text, adj_x, adj_y):
    global BASIC_FONT, DISPLAY_SURFACE

    top, left = get_top_left_of_tile(tile_x, tile_y)
    if text is None:
        pygame.draw.rect(DISPLAY_SURFACE, BLANK_TILE_COLOR, (left + adj_x, top + adj_y, TILE_SIZE, TILE_SIZE))
        text_surface = BASIC_FONT.render(str(''), ANTI_ALIASING, TEXT_COLOR)
    else:
        pygame.draw.rect(DISPLAY_SURFACE, TILE_COLOR, (left + adj_x, top + adj_y, TILE_SIZE, TILE_SIZE))
        text_surface = BASIC_FONT.render(str(text), ANTI_ALIASING, TEXT_COLOR)
    text_box = text_surface.get_rect()
    text_box.center = left + int(TILE_SIZE / 2) + adj_x, top + int(TILE_SIZE / 2) + adj_y
    DISPLAY_SURFACE.blit(text_surface, text_box)


# retrieves the x and y coordinates of the top left corner of the requested tile
# Returns (int) x, (int) y
def get_top_left_of_tile(tile_x, tile_y):
    left = X_MARGIN + (tile_x * TILE_SIZE) + (tile_x - 1)
    top = Y_MARGIN + (tile_y * TILE_SIZE) + (tile_y - 1)
    return top, left


# Updates the DISPLAY_SURFACE with the given and message
# Message will appear in the top left corner of the game
def draw_board(board, message):
    global DISPLAY_SURFACE
    if TEST_MODE:
        return
    DISPLAY_SURFACE.fill(BACK_COLOR)
    # Adds Message to DISPLAY_SURFACE if the message is not empty
    if message:
        text_surface, text_rectangle = create_text(message, MESSAGE_COLOR, BACK_COLOR, MESSAGE_Y_LOC, MESSAGE_X_LOC)
        DISPLAY_SURFACE.blit(text_surface, text_rectangle)

    # Draws All tiles on the game board
    for tile_x in range(len(board)):
        for tile_y in range(len(board[0])):
            draw_tile(tile_x, tile_y, board[tile_x][tile_y], 0, 0)

    # Draws a border around the tiles
    top, left = get_top_left_of_tile(0, 0)
    width = BOARD_WIDTH * TILE_SIZE
    height = BOARD_HEIGHT * TILE_SIZE
    pygame.draw.rect(DISPLAY_SURFACE, BORDER_COLOR, (left - 5, top - 5, width + 11, height + 11), 4)

    # Adds Reset, New Game and Solve Buttons
    DISPLAY_SURFACE.blit(RESET_GAME_SURFACE, RESET_GAME_RECT)
    DISPLAY_SURFACE.blit(NEW_GAME_SURFACE, NEW_GAME_RECT)
    DISPLAY_SURFACE.blit(SOLVE_GAME_SURFACE, SOLVE_GAME_RECT)


# Finds the Row and Column of the empty tile
# Returns (int) Col, (int) Row
def find_empty_square(board):
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y] is None:
                return x, y
    return None


# Checks if the requested move is valid in the given board
# Returns (Bool) - Valid Move = True
def is_valid_move(board, move):
    x, y = find_empty_square(board)
    return ((PlayerMoves.UP == move and y != len(board[0]) - 1) or
            (PlayerMoves.DOWN == move and y != 0) or
            (PlayerMoves.LEFT == move and len(board) - 1 != x) or
            (PlayerMoves.RIGHT == move and 0 != x))


# Updates the board based on the provided move
# the board array being sent will be modified by this function, no value is returned
def apply_move_to_board(board, move):
    x, y = find_empty_square(board)
    if move == PlayerMoves.UP:
        board[x][y], board[x][y+1] = board[x][y+1], board[x][y]
    elif move == PlayerMoves.DOWN:
        board[x][y], board[x][y-1] = board[x][y-1], board[x][y]
    elif move == PlayerMoves.LEFT:
        board[x][y], board[x+1][y] = board[x+1][y], board[x][y]
    elif move == PlayerMoves.RIGHT:
        board[x][y], board[x-1][y] = board[x-1][y], board[x][y]


# Handles the tile translation animation
def animate_move(board, move, message, animation_speed):
    global DISPLAY_SURFACE, FPS_CLOCK
    empty_x, empty_y = find_empty_square(board)
    # Determine move that is being moved to the empty square
    if move == PlayerMoves.UP:
        move_x = empty_x
        move_y = empty_y + 1
    elif move == PlayerMoves.DOWN:
        move_x = empty_x
        move_y = empty_y - 1
    elif move == PlayerMoves.LEFT:
        move_x = empty_x + 1
        move_y = empty_y
    elif move == PlayerMoves.RIGHT:
        move_x = empty_x -1
        move_y = empty_y
    else:
        move_x = empty_x
        move_y = empty_y

    if TEST_MODE:
        return
    # Prepares the base surface
    draw_board(board, message)
    board_surface = DISPLAY_SURFACE.copy()
    # Retrieves the original position of the tile being moved
    get_top_left_of_tile(move_x, move_y)
    # Translates the tile from the original position to the final position
    for i in range(0, TILE_SIZE, animation_speed):
        # Check if the user has left the game
        check_for_quit()
        # Draw board surface onto the display
        DISPLAY_SURFACE.blit(board_surface, (0, 0))
        if move == PlayerMoves.UP:
            draw_tile(move_x, move_y, board[move_x][move_y], 0, -i)
        elif move == PlayerMoves.DOWN:
            draw_tile(move_x, move_y, board[move_x][move_y], 0, i)
        elif move == PlayerMoves.LEFT:
            draw_tile(move_x, move_y, board[move_x][move_y], -i, 0)
        elif move == PlayerMoves.RIGHT:
            draw_tile(move_x, move_y, board[move_x][move_y], i, 0)
        # Update the display and wait for FPS clock
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


# Checks if a move is valid and applies the move if it is
def check_make_move(board, move, message, animation_speed):
    if move is not PlayerMoves.UNCHANGED and is_valid_move(board, move):
        # Move Animation
        if animation_speed is not None:
            animate_move(board, move, message, animation_speed)
        # Make Move
        apply_move_to_board(board, move)
        # Append Move Made by player to move count


# Retrieves the Column and Row of the tile that was clicked by the user at coordinates pos_x, pos_y
# Returns (int) Col, (int) Row
# Returns None, None if the click location is somewhere other than a tile
def get_tile_clicked(board, pos_x, pos_y):
    for tile_x in range(len(board)):
        for tile_y in range(len(board[0])):
            top, left = get_top_left_of_tile(tile_x, tile_y)
            tile_rect = pygame.Rect(left, top, TILE_SIZE, TILE_SIZE)
            if tile_rect.collidepoint(pos_x, pos_y):
                return tile_x, tile_y
    return None, None


# Generates a board that resembles a solved board
# Returns (int[][]) board
def generate_solution_board():
    board = []
    for x in range(BOARD_WIDTH):
        column = []
        for y in range(BOARD_HEIGHT):
            column.append((x + 1) + y * BOARD_WIDTH)
        board.append(column)
    board[BOARD_WIDTH - 1][BOARD_HEIGHT - 1] = None
    return board


# Creates a deep copy of a board
# returns (int[][]) board
def deep_copy_board(in_board):
    out_board = []
    for row in range(len(in_board)):
        copy_col = []
        for col in range(len(in_board[0])):
            copy_col.append(in_board[row][col])
        out_board.append(copy_col)
    return out_board


# Creates a shuffled board and a starting board used for resetting a board
# back to its initial state
# Returns (int[][]) active_board, (int[][]) start_board
def shuffle_board_from_solution(solution):
    a_board = deep_copy_board(solution) # active board
    prev_move = PlayerMoves.UNCHANGED
    animation_speed = None if TEST_MODE else int(TILE_SIZE / 2)
    for i in range(BOARD_WIDTH * BOARD_HEIGHT * 10):
        rand_num = random.randint(1, 4)
        move = PlayerMoves.UNCHANGED
        if rand_num == 1 and prev_move is not PlayerMoves.DOWN:
            move = PlayerMoves.UP
        elif rand_num == 2 and prev_move is not PlayerMoves.UP:
            move = PlayerMoves.DOWN
        elif rand_num == 3 and prev_move is not PlayerMoves.RIGHT:
            move = PlayerMoves.LEFT
        elif rand_num == 4 and prev_move is not PlayerMoves.LEFT:
            move = PlayerMoves.RIGHT
        if is_valid_move(a_board, move):
            prev_move = move
            check_make_move(a_board, move, '', animation_speed)
        else:
            i = i + 1

    start_board = deep_copy_board(a_board) # board to remain unchanged
    return a_board, start_board


# Creates a solution for the board and applies it, With animation
# Returns (int[][]) board
def solve_puzzle_a_star(board, solution_board):
    global SOLUTION_NODE, SOLVER_COMPLETE
    SOLUTION_NODE = None
    SOLVER_COMPLETE = False

    class FrontierNode:

        # Calculates an estimated distance to the goal
        # This value is intended to be less than the actual solution
        # returns (int) heuristic_value
        def calculate_hueristic(self):
            h = 0
            for x in range(len(self.board)):
                for y in range(len(self.board[0])):
                    if self.board[x][y] is not self.solve_state[x][y]:
                        h = h + 1
            return h

        # Constructor for Node Object
        def __init__(self, current_board, solution_board, parent_solution):
            self.board = current_board
            self.solve_state = solution_board
            self.solution = parent_solution
            self.heuristic_value = self.calculate_hueristic()
            self.active_cost = len(self.solution)
            self.estimated_cost = self.active_cost + self.heuristic_value

    # Finds the node with the lowest estimated cost
    # If the node with the lowest estimated cost has a heuristic value of 0 the puzzle is solved
    # Returns (FrontierNode) optimal_node, is_solved
    def check_for_optimal_solution(frontier):
        optimal_node = frontier[0]
        minimum = frontier[0].estimated_cost
        min_h = frontier[0].heuristic_value
        for i in range(len(frontier)):
            if frontier[i].estimated_cost < minimum:
                minimum = frontier[i].estimated_cost
                min_h = frontier[i].heuristic_value
                optimal_node = frontier[i]
            elif frontier[i].estimated_cost == minimum and frontier[i].heuristic_value < min_h:
                minimum = frontier[i].estimated_cost
                min_h = frontier[i].heuristic_value
                optimal_node = frontier[i]

        return optimal_node, optimal_node.heuristic_value == 0

    def create_new_node_extension(node, visited, move):
        if is_valid_move(node.board, move):
            new_solution = []
            new_solution.extend(node.solution)
            new_solution.append(move)
            new_board = deep_copy_board(node.board)
            apply_move_to_board(new_board, move)
            new_node = FrontierNode(new_board, node.solve_state, new_solution)
            if new_node.board not in visited:
                return new_node
        return None

    # Creates a list of all nodes that can be expanded off of the current node
    # boards that have already been visited will not be returned to
    # Returns (FrontierNode[]) new_nodes
    def expand_frontier(node, visited):
        new_nodes = []
        node_to_append = create_new_node_extension(node, visited, PlayerMoves.UP)
        if node_to_append is not None:
            new_nodes.append(node_to_append)
        node_to_append = create_new_node_extension(node, visited, PlayerMoves.DOWN)
        if node_to_append is not None:
            new_nodes.append(node_to_append)
        node_to_append = create_new_node_extension(node, visited, PlayerMoves.LEFT)
        if node_to_append is not None:
            new_nodes.append(node_to_append)
        node_to_append = create_new_node_extension(node, visited, PlayerMoves.RIGHT)
        if node_to_append is not None:
            new_nodes.append(node_to_append)
        return new_nodes

    # creates a list of moves to be taken in order to solve the puzzle
    # Returns (PlayerMove[]) solution
    def calculate_solution(active_board, sol_board):
        global SOLUTION_NODE, SOLVER_COMPLETE, BOARDS_ANALYZED, TERMINATED
        frontier = []
        visited_boards = [] # A* may already be optimized to not return to boards that have already been visited
        frontier.append(FrontierNode(active_board, sol_board, []))
        # loop through the solution until solution is found or until MAX_SOLUTION is reached
        BOARDS_ANALYZED = 0
        while len(frontier) > 0 and not TERMINATED:
            BOARDS_ANALYZED = BOARDS_ANALYZED + 1
            current_optimal_node, solved = check_for_optimal_solution(frontier)
            if solved:
                SOLUTION_NODE = current_optimal_node
                SOLVER_COMPLETE = True
                return
            frontier.extend(expand_frontier(current_optimal_node, visited_boards))
            visited_boards.append(current_optimal_node.board)
            frontier.remove(current_optimal_node)
        SOLUTION_NODE = None
        SOLVER_COMPLETE = True
        return

    def graphics_handler():
        global SOLVER_COMPLETE
        if TEST_MODE:
            return
        while not SOLVER_COMPLETE:
            # Handle Display Update
            draw_board(board, 'Generating Solution...    Boards Analyzed: ' + str(BOARDS_ANALYZED))
            pygame.display.update()
            FPS_CLOCK.tick(FPS)
        SOLVER_COMPLETE = False

    # Applies the solution to the board, with animation
    # Returns the board after the solution has been applied
    def apply_solution(board, solution):
        for i in range(len(solution)):
            check_make_move(board, solution[i], 'Solving...', int(TILE_SIZE/3))
        return board

    solver_thread = threading.Thread(target=calculate_solution, args=(board, solution_board))
    graphics_thread = threading.Thread(target=graphics_handler, args=())
    solver_thread.start()
    graphics_thread.start()
    solver_thread.join()
    solver_thread.join()

    if SOLUTION_NODE is not None:
        board = apply_solution(board, SOLUTION_NODE.solution)
    return board


# Creates a solution for the board and applies it, With animation
# Returns (int[][]) board
def solve_puzzle_shortest_path_first(board, solution_board):
    global SOLUTION_NODE, solver_complete
    SOLUTION_NODE = None
    SOLVER_COMPLETE = False

    class FrontierNode:
        def is_board_solved(self):
            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    if self.board[i][j] is not self.solve_state[i][j]:
                        return False
            return True

        # Constructor for Node Object
        def __init__(self, current_board, int_solution_board, parent_solution):
            self.board = current_board
            self.solve_state = int_solution_board
            self.solution = parent_solution
            self.active_cost = len(self.solution)
            self.board_is_solved = self.is_board_solved()

    # Finds the node with the lowest estimated cost
    # If the node with the lowest estimated cost has a heuristic value of 0 the puzzle is solved
    # Returns (FrontierNode) optimal_node, is_solved
    def check_for_optimal_solution(frontier):
        optimal_node = frontier[0]
        minimum = frontier[0].active_cost
        for i in range(len(frontier)):
            if frontier[i].active_cost < minimum:
                minimum = frontier[i].active_cost
                optimal_node = frontier[i]
        return optimal_node

    def create_new_node_extension(node, visited, move):
        if is_valid_move(node.board, move):
            new_solution = []
            new_solution.extend(node.solution)
            new_solution.append(move)
            new_board = deep_copy_board(node.board)
            apply_move_to_board(new_board, move)
            new_node = FrontierNode(new_board, node.solve_state, new_solution)
            if new_node.board not in visited:
                return new_node
        return None

    # Creates a list of all nodes that can be expanded off of the current node
    # boards that have already been visited will not be returned to
    # Returns (FrontierNode[]) new_nodes
    def expand_frontier(node, visited):
        new_nodes = []
        node_to_append = create_new_node_extension(node, visited, PlayerMoves.UP)
        if node_to_append is not None:
            new_nodes.append(node_to_append)
        node_to_append = create_new_node_extension(node, visited, PlayerMoves.DOWN)
        if node_to_append is not None:
            new_nodes.append(node_to_append)
        node_to_append = create_new_node_extension(node, visited, PlayerMoves.LEFT)
        if node_to_append is not None:
            new_nodes.append(node_to_append)
        node_to_append = create_new_node_extension(node, visited, PlayerMoves.RIGHT)
        if node_to_append is not None:
            new_nodes.append(node_to_append)
        return new_nodes

    # creates a list of moves to be taken in order to solve the puzzle
    # Returns (PlayerMove[]) solution
    def calculate_solution(active_board, sol_board):
        global SOLUTION_NODE, SOLVER_COMPLETE, BOARDS_ANALYZED, TERMINATED
        frontier = []
        visited_boards = [] # A* may already be optimized to not return to boards that have already been visited
        frontier.append(FrontierNode(active_board, sol_board, []))
        # loop through the solution until solution is found or until MAX_SOLUTION is reached
        BOARDS_ANALYZED = 0
        while len(frontier) > 0 and not TERMINATED:
            BOARDS_ANALYZED = BOARDS_ANALYZED + 1
            current_optimal_node = check_for_optimal_solution(frontier)
            if current_optimal_node.board_is_solved:
                SOLUTION_NODE = current_optimal_node
                SOLVER_COMPLETE = True
                return
            frontier.extend(expand_frontier(current_optimal_node, visited_boards))
            visited_boards.append(current_optimal_node.board)
            frontier.remove(current_optimal_node)
        SOLUTION_NODE = None
        SOLVER_COMPLETE = True
        return

    def graphics_handler():
        global SOLVER_COMPLETE
        if TEST_MODE:
            return
        while not SOLVER_COMPLETE:
            # Handle Display Update
            draw_board(board, 'Generating Solution...    Boards Analyzed: ' + str(BOARDS_ANALYZED))
            pygame.display.update()
            FPS_CLOCK.tick(FPS)
        SOLVER_COMPLETE = False

    # Applies the solution to the board, with animation
    # Returns the board after the solution has been applied
    def apply_solution(board, solution):
        for i in range(len(solution)):
            check_make_move(board, solution[i], 'Solving...', int(TILE_SIZE/3))
        return board

    solver_thread = threading.Thread(target=calculate_solution, args=(board, solution_board))
    graphics_thread = threading.Thread(target=graphics_handler, args=())
    solver_thread.start()
    graphics_thread.start()
    solver_thread.join()
    solver_thread.join()

    if SOLUTION_NODE is not None:
        board = apply_solution(board, SOLUTION_NODE.solution)
    return board


# Handles W-A-S-D and Arrow key press events for player moves
# Returns (PlayerMove) selected_move
def handle_key_press_event(board, event):
    if event.key in (K_LEFT, K_a) and is_valid_move(board, PlayerMoves.LEFT):
        selected_move = PlayerMoves.LEFT
    elif event.key in (K_RIGHT, K_d) and is_valid_move(board, PlayerMoves.RIGHT):
        selected_move = PlayerMoves.RIGHT
    elif event.key in (K_UP, K_w) and is_valid_move(board, PlayerMoves.UP):
        selected_move = PlayerMoves.UP
    elif event.key in (K_DOWN, K_s) and is_valid_move(board, PlayerMoves.DOWN):
        selected_move = PlayerMoves.DOWN
    else:
        selected_move = PlayerMoves.UNCHANGED
    return selected_move


# Handles mouse click events for player option selection
# Reset Game - updates board back to starting board
# New Game - Updates Board to a New board shuffle - starting board updated to New board Shuffle
# Solve Game - Creates a solution for the game and applies the solution via animation
# returns (int[][]) active_board, (int[][]) starting_board
def handle_options_clicked_event(board, starting_board, solution_board, event_position):
    if RESET_GAME_RECT.collidepoint(event_position):
        board = deep_copy_board(starting_board)
    elif NEW_GAME_RECT.collidepoint(event_position):
        board, starting_board = shuffle_board_from_solution(deep_copy_board(solution_board))
    elif SOLVE_GAME_RECT.collidepoint(event_position):
        if SOLUTION_METHOD is 0:
            board = solve_puzzle_shortest_path_first(board, solution_board)
        elif SOLUTION_METHOD is 1:
            board = solve_puzzle_a_star(board, solution_board)
    return board, starting_board


# Handles mouse click events for player moves
# Returns (PlayerMove) Selected_move
def handle_tile_clicked_event(board, click_x, click_y):
    empty_x, empty_y = find_empty_square(board)
    if click_x == empty_x and click_y == empty_y + 1:
        selected_move = PlayerMoves.UP
    elif click_x == empty_x and click_y == empty_y - 1:
        selected_move = PlayerMoves.DOWN
    elif click_x == empty_x + 1 and click_y == empty_y:
        selected_move = PlayerMoves.LEFT
    elif click_x == empty_x - 1 and click_y == empty_y:
        selected_move = PlayerMoves.RIGHT
    else:
        selected_move = PlayerMoves.UNCHANGED
    return selected_move


# Handles main game logic and graphics loop
# Exits on player Quit
def game_loop(board, starting_board, solution_board):
    while True:
        selected_move = PlayerMoves.UNCHANGED
        message = '' # Contains the message to show in the upper left corner
        # Check if the player has won
        if board == solution_board:
            message = 'Solved!'

        # Draw the current iteration of the board, Provide a message if they have won
        draw_board(board, message)

        # Check if the player has 'Quit'
        check_for_quit()

        # Check for events to be handled
        for event in pygame.event.get():
            # Handle clicked events
            if event.type == MOUSEBUTTONUP:
                test = 2
            # Handle Key Released Events
            # Check if user pressed a Key to move a tile W-A-S-D and Arrow Keys enabled
            if event.type == KEYUP:
                selected_move = handle_key_press_event(board, event)
            elif event.type == MOUSEBUTTONUP:
                click_x, click_y = get_tile_clicked(board, event.pos[0], event.pos[1])
                if (click_x, click_y) == (None, None):
                    board, starting_board = handle_options_clicked_event(board, starting_board, solution_board, event.pos)
                else:
                    selected_move = handle_tile_clicked_event(board, click_x, click_y)
        # Process Move Selection
        check_make_move(board, selected_move, message,  int(TILE_SIZE / 4))

        # Handle Display Update
        pygame.display.update()
        FPS_CLOCK.tick(FPS)

    return pygame


def main():
    global FPS_CLOCK, DISPLAY_SURFACE, BASIC_FONT, RESET_GAME_SURFACE, RESET_GAME_RECT, NEW_GAME_SURFACE, \
        NEW_GAME_RECT, SOLVE_GAME_SURFACE, SOLVE_GAME_RECT

    # Initializes global board parameter values
    def setup():
        global FPS_CLOCK, DISPLAY_SURFACE, BASIC_FONT, RESET_GAME_SURFACE, RESET_GAME_RECT, NEW_GAME_SURFACE, \
            NEW_GAME_RECT, SOLVE_GAME_SURFACE, SOLVE_GAME_RECT

        pygame.init()
        FPS_CLOCK = pygame.time.Clock()
        DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)
                                              )
        pygame.display.set_caption('Slide Puzzle')
        BASIC_FONT = pygame.font.Font('freesansbold.ttf', BASIC_FONT_SIZE)
        RESET_GAME_SURFACE, RESET_GAME_RECT = create_text('Reset', TEXT_COLOR, TILE_COLOR, (WINDOW_WIDTH / 3) - 160, WINDOW_HEIGHT - 50)
        NEW_GAME_SURFACE, NEW_GAME_RECT = create_text('New Game', TEXT_COLOR, TILE_COLOR, ((2 * WINDOW_WIDTH ) / 3 ) - 160, WINDOW_HEIGHT - 50)
        SOLVE_GAME_SURFACE, SOLVE_GAME_RECT = create_text('Solve Game', TEXT_COLOR, TILE_COLOR, WINDOW_WIDTH - 160, WINDOW_HEIGHT - 50)

        NEW_GAME_RECT, SOLVE_GAME_SURFACE, SOLVE_GAME_RECT

    setup()                                                                     # Initialize game variables
    solution_board = generate_solution_board()                                  # Creates a general Solution board
    active_board, starting_board = shuffle_board_from_solution(solution_board)  # Creates initial Board
    game_loop(active_board, starting_board, solution_board)                     # Start Main game loop


if __name__ == '__main__':
    main()
