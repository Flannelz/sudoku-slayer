from sudoku import Sudoku
from constraint import backtrack

example_input = [0, 0, 4, 3, 0, 0, 2, 0, 9, 0, 0, 5, 0, 0, 9, 0, 0, 1, 0, 7, 0, 0, 6, 0, 0, 4, 3, 0, 0, 6, 0, 0, 2, 0, 8, 7, 1, 9, 0, 0, 0, 7, 4, 0, 0, 0, 5, 0, 0, 8, 3, 0, 0, 0, 6, 0, 0, 0, 0, 0, 1, 0, 5, 0, 0, 3, 5, 0, 8, 6, 9, 0, 0, 4, 2, 9, 1, 0, 3, 0, 0]
example_puzzle = Sudoku(example_input)

def test1():
    assert example_puzzle.get_variables('A3') == 4

def test2():
    assert example_puzzle.get_neighbors('A3') == ['A1', 'A2', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'I3', 'B1', 'B2', 'C1', 'C2']

def test3():
    assert example_puzzle.get_domains('A3') == []

def test_4():
    assert example_puzzle.constraints_check() == True

def test_5():
    assert example_puzzle.goal_check() == False

def test6():
    assert example_puzzle.export_grid() == example_input