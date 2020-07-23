import py_slider
py_slider.TEST_MODE = True
py_slider.BOARD_HEIGHT = 3
py_slider.BOARD_WIDTH = 3
py_slider.TILE_SIZE = 90

# "pytest board_logic_unit_tests.py" can be called to run all board logic tests
# -r A can be added as an argument to display all test cases (Pass/Fail/Skip)


#
#   get_top_left_of_tile test cases
#
def test_get_top_left_center_tile():
    expected_left = py_slider.X_MARGIN + py_slider.TILE_SIZE
    expected_top = py_slider.Y_MARGIN + py_slider.TILE_SIZE
    top, left = py_slider.get_top_left_of_tile(1, 1)
    assert expected_top == top
    assert expected_left == left


def test_get_top_left_edge_tile():
    expected_left = py_slider.X_MARGIN + py_slider.TILE_SIZE
    expected_top = py_slider.Y_MARGIN - 1
    top, left = py_slider.get_top_left_of_tile(1, 0)
    assert expected_top == top
    assert expected_left == left


def test_get_top_left_corner_tile():
    expected_left = py_slider.X_MARGIN - 1
    expected_top = py_slider.Y_MARGIN - 1
    top, left = py_slider.get_top_left_of_tile(0, 0)
    assert expected_top == top
    assert expected_left == left


#
#   find_empty_square test cases
#
def test_find_empty_square_corner_tile():
    # # # # # # # # #
    #   1       6   #
    #   2   4   7   #
    #   3   5   8   #
    # # # # # # # # #
    board = [[None, 2, 3], [4, 5, 6], [7, 8, 9]]
    expected_row = 0
    expected_col = 0
    row, col = py_slider.find_empty_square(board)
    assert expected_col == col
    assert expected_row == row


def test_find_empty_square_edge_tile():
    # # # # # # # # #
    #   1       6   #
    #   2   4   7   #
    #   3   5   8   #
    # # # # # # # # #
    board = [[1, 2, 3], [None, 4, 5], [6, 7, 8]]
    expected_row = 1
    expected_col = 0
    row, col = py_slider.find_empty_square(board)
    assert expected_col == col
    assert expected_row == row


def test_find_empty_square_center_tile():
    # # # # # # # # #
    #   1   4   6   #
    #   2       7   #
    #   3   5   8   #
    # # # # # # # # #
    board = [[1, 2, 3], [4, None, 5], [6, 7, 8]]
    expected_row = 1
    expected_col = 1
    row, col = py_slider.find_empty_square(board)
    assert expected_col == col
    assert expected_row == row


#
#   is_valid_move test cases
#
def test_is_not_valid_move_br_corner_up():
    # # # # # # # # #
    #   1   4   7   #
    #   2   5   8   #
    #   3   6       #
    # # # # # # # # #
    board = [[1, 2, 3], [4, 5, 6], [7, 8, None]]
    assert not py_slider.is_valid_move(board, py_slider.PlayerMoves.UP)


def test_is_valid_move_br_corner_down():
    # # # # # # # # #
    #   1   4   7   #
    #   2   5   8   #
    #   3   6       #
    # # # # # # # # #
    board = [[1, 2, 3], [4, 5, 6], [7, 8, None]]
    assert py_slider.is_valid_move(board, py_slider.PlayerMoves.DOWN)


def test_is_not_valid_move_br_corner_left():
    # # # # # # # # #
    #   1   4   7   #
    #   2   5   8   #
    #   3   6       #
    # # # # # # # # #
    board = [[1, 2, 3], [4, 5, 6], [7, 8, None]]
    assert not py_slider.is_valid_move(board, py_slider.PlayerMoves.LEFT)


def test_is_valid_move_br_corner_right():
    # # # # # # # # #
    #   1   4   7   #
    #   2   5   8   #
    #   3   6       #
    # # # # # # # # #
    board = [[1, 2, 3], [4, 5, 6], [7, 8, None]]
    assert py_slider.is_valid_move(board, py_slider.PlayerMoves.RIGHT)


def test_is_valid_move_center_up():
    # # # # # # # # #
    #   1   4   6   #
    #   2       7   #
    #   3   5   8   #
    # # # # # # # # #
    board = [[1, 2, 3], [4, None, 5], [6, 7, 8]]
    assert py_slider.is_valid_move(board, py_slider.PlayerMoves.UP)


def test_is_valid_move_center_down():
    # # # # # # # # #
    #   1   4   6   #
    #   2       7   #
    #   3   5   8   #
    # # # # # # # # #
    board = [[1, 2, 3], [4, None, 5], [6, 7, 8]]
    assert py_slider.is_valid_move(board, py_slider.PlayerMoves.DOWN)


def test_is_valid_move_center_left():
    # # # # # # # # #
    #   1   4   6   #
    #   2       7   #
    #   3   5   8   #
    # # # # # # # # #
    board = [[1, 2, 3], [4, None, 5], [6, 7, 8]]
    assert py_slider.is_valid_move(board, py_slider.PlayerMoves.LEFT)


def test_is_valid_move_center_right():
    # # # # # # # # #
    #   1   4   6   #
    #   2       7   #
    #   3   5   8   #
    # # # # # # # # #
    board = [[1, 2, 3], [4, None, 5], [6, 7, 8]]
    assert py_slider.is_valid_move(board, py_slider.PlayerMoves.RIGHT)


#
#   apply_move_to_board test cases
#
def test_apply_move_to_board_up():
    # # # # # # # # #
    #   1   2   3   #
    #   4   5       #
    #   7   8   6   #
    # # # # # # # # #
    board = [[1, 4, 7],[2, 5, 8],[3, None, 6]]
    # # # # # # # # #
    #   1   2   3   #
    #   4   5   6   #
    #   7   8       #
    # # # # # # # # #
    expected_board = [[1, 4, 7],[2, 5, 8],[3, 6, None]]
    py_slider.apply_move_to_board(board, py_slider.PlayerMoves.UP)
    assert board == expected_board


def test_apply_move_to_board_down():
    # # # # # # # # #
    #   1   2   3   #
    #   4   5   6   #
    #   7   8       #
    # # # # # # # # #
    board = [[1, 4, 7],[2, 5, 8],[3, 6, None]]
    # # # # # # # # #
    #   1   2   3   #
    #   4   5       #
    #   7   8   6   #
    # # # # # # # # #
    expected_board = [[1, 4, 7],[2, 5, 8],[3, None, 6]]
    py_slider.apply_move_to_board(board, py_slider.PlayerMoves.DOWN)
    assert board == expected_board


def test_apply_move_to_board_left():
    # # # # # # # # #
    #   1   2   3   #
    #   4   5   6   #
    #   7       8   #
    # # # # # # # # #
    board = [[1, 4, 7],[2, 5, None],[3, 6, 8]]
    # # # # # # # # #
    #   1   2   3   #
    #   4   5   6   #
    #   7   8       #
    # # # # # # # # #
    expected_board = [[1, 4, 7],[2, 5, 8],[3, 6, None]]
    py_slider.apply_move_to_board(board, py_slider.PlayerMoves.LEFT)
    assert board == expected_board


def test_apply_move_to_board_right():
    # # # # # # # # #
    #   1   2   3   #
    #   4   5   6   #
    #   7   8       #
    # # # # # # # # #
    board = [[1, 4, 7],[2, 5, 8],[3, 6, None]]
    # # # # # # # # #
    #   1   2   3   #
    #   4   5   6   #
    #   7       8   #
    # # # # # # # # #
    expected_board = [[1, 4, 7],[2, 5, None],[3, 6, 8]]
    py_slider.apply_move_to_board(board, py_slider.PlayerMoves.RIGHT)
    assert board == expected_board


#
#   check_make_move test cases
#
def test_check_make_move_up():
    # # # # # # # # #
    #   1   2   3   #
    #   4   5   6   #
    #   7   8       #
    # # # # # # # # #
    board = [[1, 4, 7],[2, 5, 8],[3, 6, None]]
    # # # # # # # # #
    #   1   2   3   #
    #   4   5   6   #
    #   7   8       #
    # # # # # # # # #
    expected_board = [[1, 4, 7],[2, 5, 8],[3, 6, None]]
    py_slider.check_make_move(board, py_slider.PlayerMoves.UP, "", None)
    assert board == expected_board


def test_check_make_move_down():
    # # # # # # # # #
    #   1   2   3   #
    #   4   5   6   #
    #   7   8       #
    # # # # # # # # #
    board = [[1, 4, 7],[2, 5, 8],[3, 6, None]]
    # # # # # # # # #
    #   1   2   3   #
    #   4   5       #
    #   7   8   6   #
    # # # # # # # # #
    expected_board = [[1, 4, 7],[2, 5, 8],[3, None, 6]]
    py_slider.check_make_move(board, py_slider.PlayerMoves.DOWN, "", None)
    assert board == expected_board


def test_check_make_move_left():
    # # # # # # # # #
    #   1   2   3   #
    #   4   5   6   #
    #   7   8       #
    # # # # # # # # #
    board = [[1, 4, 7],[2, 5, 8],[3, 6, None]]
    # # # # # # # # #
    #   1   2   3   #
    #   4   5   6   #
    #   7   8       #
    # # # # # # # # #
    expected_board = [[1, 4, 7],[2, 5, 8],[3, 6, None]]
    py_slider.check_make_move(board, py_slider.PlayerMoves.LEFT, "", None)
    assert board == expected_board


def test_check_make_move_right():
    # # # # # # # # #
    #   1   2   3   #
    #   4   5   6   #
    #   7   8       #
    # # # # # # # # #
    board = [[1, 4, 7],[2, 5, 8],[3, 6, None]]
    # # # # # # # # #
    #   1   2   3   #
    #   4   5   6   #
    #   7       8   #
    # # # # # # # # #
    expected_board = [[1, 4, 7],[2, 5, None],[3, 6, 8]]
    py_slider.check_make_move(board, py_slider.PlayerMoves.RIGHT, "", None)
    assert board == expected_board


#
#   get_tile_clicked test cases
#
def test_get_tile_clicked_tc():
    # # # # # # # # #
    #  [1]  2   3   #
    #   4   5   6   #
    #   7   8       #
    # # # # # # # # #
    board = [[1, 4, 7], [2, 5, 8], [3, 6, None]]
    tile_x, tile_y = 0, 0
    top, left = py_slider.get_top_left_of_tile(tile_x, tile_y)
    top = top + py_slider.TILE_SIZE/2
    left = left + py_slider.TILE_SIZE/2
    expected_tile_x, expected_tile_y = py_slider.get_tile_clicked(board, left, top)
    assert expected_tile_x == 0
    assert expected_tile_y == 0


def test_get_tile_clicked_tc():
    # # # # # # # # #
    #   1  [2]  3   #
    #   4   5   6   #
    #   7   8       #
    # # # # # # # # #
    board = [[1, 4, 7], [2, 5, 8], [3, 6, None]]
    tile_x, tile_y = 1, 0
    top, left = py_slider.get_top_left_of_tile(tile_x, tile_y)
    top = top + py_slider.TILE_SIZE/2
    left = left + py_slider.TILE_SIZE/2
    expected_tile_x, expected_tile_y = py_slider.get_tile_clicked(board, left, top)
    assert expected_tile_x == 1
    assert expected_tile_y == 0


def test_get_tile_clicked_tr():
    # # # # # # # # #
    #   1   2  [3]  #
    #   4   5   6   #
    #   7   8       #
    # # # # # # # # #
    board = [[1, 4, 7], [2, 5, 8], [3, 6, None]]
    tile_x, tile_y = 2, 0
    top, left = py_slider.get_top_left_of_tile(tile_x, tile_y)
    top = top + py_slider.TILE_SIZE/2
    left = left + py_slider.TILE_SIZE/2
    expected_tile_x, expected_tile_y = py_slider.get_tile_clicked(board, left, top)
    assert expected_tile_x == 2
    assert expected_tile_y == 0


def test_get_tile_clicked_cl():
    # # # # # # # # #
    #   1   2   3   #
    #  [4]  5   6   #
    #   7   8       #
    # # # # # # # # #
    board = [[1, 4, 7], [2, 5, 8], [3, 6, None]]
    tile_x, tile_y = 0, 1
    top, left = py_slider.get_top_left_of_tile(tile_x, tile_y)
    top = top + py_slider.TILE_SIZE/2
    left = left + py_slider.TILE_SIZE/2
    expected_tile_x, expected_tile_y = py_slider.get_tile_clicked(board, left, top)
    assert expected_tile_x == 0
    assert expected_tile_y == 1


def test_get_tile_clicked_cc():
    # # # # # # # # #
    #   1   2   3   #
    #   4  [5]  6   #
    #   7   8       #
    # # # # # # # # #
    board = [[1, 4, 7], [2, 5, 8], [3, 6, None]]
    tile_x, tile_y = 1, 1
    top, left = py_slider.get_top_left_of_tile(tile_x, tile_y)
    top = top + py_slider.TILE_SIZE/2
    left = left + py_slider.TILE_SIZE/2
    expected_tile_x, expected_tile_y = py_slider.get_tile_clicked(board, left, top)
    assert expected_tile_x == 1
    assert expected_tile_y == 1


def test_get_tile_clicked_cr():
    # # # # # # # # #
    #   1   2   3   #
    #   4   5  [6]  #
    #   7   8       #
    # # # # # # # # #
    board = [[1, 4, 7], [2, 5, 8], [3, 6, None]]
    tile_x, tile_y = 2, 1
    top, left = py_slider.get_top_left_of_tile(tile_x, tile_y)
    top = top + py_slider.TILE_SIZE/2
    left = left + py_slider.TILE_SIZE/2
    expected_tile_x, expected_tile_y = py_slider.get_tile_clicked(board, left, top)
    assert expected_tile_x == 2
    assert expected_tile_y == 1


def test_get_tile_clicked_bl():
    # # # # # # # # #
    #   1   2   3   #
    #   4   5   6   #
    #  [7]  8       #
    # # # # # # # # #
    board = [[1, 4, 7], [2, 5, 8], [3, 6, None]]
    tile_x, tile_y = 0, 2
    top, left = py_slider.get_top_left_of_tile(tile_x, tile_y)
    top = top + py_slider.TILE_SIZE/2
    left = left + py_slider.TILE_SIZE/2
    expected_tile_x, expected_tile_y = py_slider.get_tile_clicked(board, left, top)
    assert expected_tile_x == 0
    assert expected_tile_y == 2


def test_get_tile_clicked_bc():
    # # # # # # # # #
    #   1   2   3   #
    #   4   5   6   #
    #   7  [8]      #
    # # # # # # # # #
    board = [[1, 4, 7], [2, 5, 8], [3, 6, None]]
    tile_x, tile_y = 1, 2
    top, left = py_slider.get_top_left_of_tile(tile_x, tile_y)
    top = top + py_slider.TILE_SIZE/2
    left = left + py_slider.TILE_SIZE/2
    expected_tile_x, expected_tile_y = py_slider.get_tile_clicked(board, left, top)
    assert expected_tile_x == 1
    assert expected_tile_y == 2


def test_get_tile_clicked_br():
    # # # # # # # # #
    #   1   2   3   #
    #   4   5   6   #
    #   7   8  [ ]  #
    # # # # # # # # #
    board = [[1, 4, 7], [2, 5, 8], [3, 6, None]]
    tile_x, tile_y = 2, 2
    top, left = py_slider.get_top_left_of_tile(tile_x, tile_y)
    top = top + py_slider.TILE_SIZE/2
    left = left + py_slider.TILE_SIZE/2
    expected_tile_x, expected_tile_y = py_slider.get_tile_clicked(board, left, top)
    assert expected_tile_x == 2
    assert expected_tile_y == 2


#
#   generate_solution_board test cases
#
def test_generate_solution_board_3x3():
    initial_board_size = (py_slider.BOARD_WIDTH, py_slider.BOARD_HEIGHT)
    py_slider.BOARD_HEIGHT = 3
    py_slider.BOARD_WIDTH = 3
    # # # # # # # # #
    #   1   2   3   #
    #   4   5   6   #
    #   7   8       #
    # # # # # # # # #
    expected_board = [[1, 4, 7],
                      [2, 5, 8],
                      [3, 6, None]]
    board = py_slider.generate_solution_board()
    assert expected_board == board
    py_slider.BOARD_WIDTH = initial_board_size[0]
    py_slider.BOARD_HEIGHT = initial_board_size[1]


def test_generate_solution_board_3x4():
    initial_board_size = (py_slider.BOARD_WIDTH, py_slider.BOARD_HEIGHT)
    py_slider.BOARD_WIDTH = 3
    py_slider.BOARD_HEIGHT = 4
    # # # # # # # # #
    #   1   2   3   #
    #   4   5   6   #
    #   7   8   9   #
    #   10  11      #
    # # # # # # # # #
    expected_board = [[1, 4, 7, 10],
                      [2, 5, 8, 11],
                      [3, 6, 9, None]]
    board = py_slider.generate_solution_board()
    assert expected_board == board
    py_slider.BOARD_WIDTH = initial_board_size[0]
    py_slider.BOARD_HEIGHT = initial_board_size[1]


def test_generate_solution_board_4x3():
    initial_board_size = (py_slider.BOARD_WIDTH, py_slider.BOARD_HEIGHT)
    py_slider.BOARD_WIDTH = 4
    py_slider.BOARD_HEIGHT = 3
    # # # # # # # # # # #
    #   1   2   3   4   #
    #   5   6   7   8   #
    #   9   10  11      #
    # # # # # # # # # # #
    expected_board = [[1, 5, 9],
                      [2, 6, 10],
                      [3, 7, 11],
                      [4, 8, None]]
    board = py_slider.generate_solution_board()
    assert expected_board == board
    py_slider.BOARD_WIDTH = initial_board_size[0]
    py_slider.BOARD_HEIGHT = initial_board_size[1]


def test_generate_solution_board_4x4():
    initial_board_size = (py_slider.BOARD_WIDTH, py_slider.BOARD_HEIGHT)
    py_slider.BOARD_WIDTH = 4
    py_slider.BOARD_HEIGHT = 4
    # # # # # # # # # # #
    #   1   2   3   4   #
    #   5   6   7   8   #
    #   9   10  11  12  #
    #   13  14  15      #
    # # # # # # # # # # #
    expected_board = [[1, 5, 9, 13],
                      [2, 6, 10, 14],
                      [3, 7, 11, 15],
                      [4, 8, 12, None]]
    board = py_slider.generate_solution_board()
    assert expected_board == board
    py_slider.BOARD_WIDTH = initial_board_size[0]
    py_slider.BOARD_HEIGHT = initial_board_size[1]


def test_generate_solution_board_6x6():
    initial_board_size = (py_slider.BOARD_WIDTH, py_slider.BOARD_HEIGHT)
    py_slider.BOARD_WIDTH = 6
    py_slider.BOARD_HEIGHT = 6
    # # # # # # # # # # # # # # #
    #   1   2   3   4   5   6   #
    #   7   8   9   10  11  12  #
    #   13  14  15  16  17  18  #
    #   19  20  21  22  23  24  #
    #   25  26  27  28  29  30  #
    #   31  32  33  34  35  36  #
    # # # # # # # # # # # # # # #
    expected_board = [[1, 7, 13, 19, 25, 31],
                      [2, 8, 14, 20, 26, 32],
                      [3, 9, 15, 21, 27, 33],
                      [4, 10, 16, 22, 28, 34],
                      [5, 11, 17, 23, 29, 35],
                      [6, 12, 18, 24, 30, None]]
    board = py_slider.generate_solution_board()
    assert expected_board == board
    py_slider.BOARD_WIDTH = initial_board_size[0]
    py_slider.BOARD_HEIGHT = initial_board_size[1]


#
#   deep_copy_board test cases
#
def test_deep_copy_board():
    # # # # # # # # #
    #   1   2   3   #
    #   4   5   6   #
    #   7   8       #
    # # # # # # # # #
    board = [[1, 4, 7],
             [2, 5, 8],
             [3, 6, None]]
    copied_board = py_slider.deep_copy_board(board)
    assert board == copied_board
    py_slider.check_make_move(board, py_slider.PlayerMoves.DOWN, "", None)
    assert board is not copied_board
    py_slider.check_make_move(board, py_slider.PlayerMoves.UP, "", None)
    py_slider.check_make_move(copied_board, py_slider.PlayerMoves.DOWN, "", None)
    assert board is not copied_board


#
#   handle_tile_clicked_event test cases
#
def test_handle_tile_clicked_event_move_up():
    # # # # # # # # #
    #   1   2   3   #
    #   4       5   #
    #   6   7   8   #
    # # # # # # # # #
    board = [[1, 4, 6], [2, None, 7], [3, 5, 8]]
    selected_move = py_slider.handle_tile_clicked_event(board, 1, 2)
    assert selected_move == py_slider.PlayerMoves.UP


def test_handle_tile_clicked_event_move_down():
    # # # # # # # # #
    #   1   2   3   #
    #   4       5   #
    #   6   7   8   #
    # # # # # # # # #
    board = [[1, 4, 6], [2, None, 7], [3, 5, 8]]
    selected_move = py_slider.handle_tile_clicked_event(board, 1, 0)
    assert selected_move == py_slider.PlayerMoves.DOWN


def test_handle_tile_clicked_event_move_left():
    # # # # # # # # #
    #   1   2   3   #
    #   4       5   #
    #   6   7   8   #
    # # # # # # # # #
    board = [[1, 4, 6], [2, None, 7], [3, 5, 8]]
    selected_move = py_slider.handle_tile_clicked_event(board, 2, 1)
    assert selected_move == py_slider.PlayerMoves.LEFT


def test_handle_tile_clicked_event_move_right():
    # # # # # # # # #
    #   1   2   3   #
    #   4       5   #
    #   6   7   8   #
    # # # # # # # # #
    board = [[1, 4, 6], [2, None, 7], [3, 5, 8]]
    selected_move = py_slider.handle_tile_clicked_event(board, 0, 1)
    assert selected_move == py_slider.PlayerMoves.RIGHT


def test_handle_tile_clicked_event_unchanged():
    # # # # # # # # #
    #   1   2   3   #
    #   4   5   6   #
    #   7   8       #
    # # # # # # # # #
    board = [[1, 4, 7], [2, 5, 8], [3, 6, None]]
    selected_move = py_slider.handle_tile_clicked_event(board, 0, 0)
    assert selected_move == py_slider.PlayerMoves.UNCHANGED