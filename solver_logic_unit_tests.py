import py_slider
import pytest
import warnings
import time

# "pytest solver_logic_unit_tests.py" can be called to run all board logic tests
# -r A can be added as an argument to display all test cases (Pass/Fail/Skip)


py_slider.TEST_MODE = True
py_slider.BOARD_HEIGHT = 3
py_slider.BOARD_WIDTH = 3
py_slider.TILE_SIZE = 90
EFFICIENCY_SOLUTIONS = 8
EFFICIENCY_MAX_TIME = 20

#
#   solve_puzzle_a_star logic test case
#
def test_solve_puzzle_a_star_logic(thread_number=None):
    # # # # # # # # #
    #   1   2   3   #
    #   4   5   6   #
    #   7   8       #
    # # # # # # # # #
    start_time = time.time()
    solution_board = py_slider.generate_solution_board()
    board, unused = py_slider.shuffle_board_from_solution(solution_board)
    py_slider.solve_puzzle_a_star(board, solution_board)
    assert board == solution_board
    if thread_number is not None:
        print("Run Time for thread #" + str(thread_number)+ ": " + str(time.time() - start_time))

#
#   solve_puzzle_a_star efficiency test case
#
def test_solve_puzzle_a_start_efficiency():
    import threading
    threads = list()

    for index in range(EFFICIENCY_SOLUTIONS):
        x = threading.Thread(target=test_solve_puzzle_a_star_logic, args=(), kwargs={'thread_number': index})
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        thread.join()
        print("Thread #" + str(index) + " Joined")
