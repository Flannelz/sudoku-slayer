# File: constraints.py
# Author: Alice Hanigan
# Date: 04/10/2020
#

import value
from sudoku import Sudoku

def f(value_grid):

    return True

def g(value_grid):

    return value_grid

class Constraint:
    # A class for a constraint to apply to a CSP like a Sudoku puzzle
    # Fields:
    # string: a String representation of the constraint, used to determine its type
    # check_function: the function called on a ValueGrid to determine whether the constraint is satisfied
    # enforce_function: a function called on a ValueGrid to enforce the constraint, if trivially possible (i.e. for unary constraints and arcs)
    #
    # For a very simple Constraint representation, set the string to "Unary" if the constraint is unary, to "Binary" if it is binary, or to "" if it is neither
    # Unary constraints *must* have enforce functions to work properly
    # Binary and other constraints do not need this function currently

    def __init__(self, string="", func=f, g=None):
        self.string = string
        self.check_function = func
        self.enforce_function = g

    def to_string(self):

        return self.string

    def check(self, value_grid):

        return self.check_function(value_grid)

    def enforce(self, value_grid):

        if self.enforce_function == None:

            return value_grid

        else:

            return self.enforce_function(value_grid)

    def get_type(self):

        return get_constraint_type(self.to_string())

def get_constraint_type(string):
    # TODO: define other types?

    if "Unary" in string:

        return "Unary"

    if ("Binary" in string) or ("Arc" in string):

        return "Binary"

    else:

        return "Other"

class SudokuError(Exception):
    # Gives us a custom Exception for errors related to the Sudoku problem representation
    
    pass

def apply_unary_constraints(constraints, value_grid):
    # Takes a list of Constraint objects and a ValueGrid, and applies all unary constraints to the ValueGrid

    for constraint in constraints:

        if constraint.get_type() == "Unary":

            value_grid = constraint.enforce(value_grid)
            constraints.remove(constraint)

    return (constraints, value_grid)

# I'm not sure we need these now that the Sudoku class contains the _neighbors dictionary
# def arc_consistency(sudoku):
#     # Enforces arc consistency on the ValueGrid, by applying the binary constraints in the list of Constraint objects

#     arcs = generate_arcs(value_grid)

#     for arc in arcs:

#         for possible in value_grid.get_guesses(arc[0]):

#             for constraint in constraints:

#                 if constraint.get_type() != "Binary":

#                     pass

#                 elif not constraint.check(value_grid.guess(arc[0], possible)):

#                     value_grid.remove_guess(arc[0], possible)
#                     break

#         if len(value_grid.get_guesses(arc[0])) == 0:

#             raise SudokuError("No possible values left for", arc[0], "when enforcing arc consistency")

#         if len(value_grid.get_guesses(arc[0])) == 1:

#             value_grid.set_value(arc[0], value_grid.get_guesses(arc[0])[0])
            
#     return value_grid

#def generate_arcs(sudoku):
    # TODO: create a function that generates a list of all pairs of indices of *neighbors* in the ValueGrid object

def backtrack(sudoku):
    # Oder with Minimum Remaining Values(MRV)
    # Use MAC algorithm for failure checking
    
    # Returns a list of all possible cells with the smallest number of possible values
    def MRV(sudoku):
        cell_domains = sudoku.get_domains()
        min_values = float('inf')
        candidates = []
        for cell in cell_domains:
            if len(cell_domains[cell]) < min_values and len(cell_domains[cell]) > 0:
                min_values = len(cell_domains[cell])
                candidates = [cell]
            elif len(cell_domains[cell]) == min_values:
                candidates.append(cell)
        return candidates

    def recursive_backtrack(sudoku, test_sudoku):
        if test_sudoku.goal_check():
            return True
        var = MRV(test_sudoku)[0]
        test_domain = test_sudoku.get_domains(var)
        for value in test_domain:
            test_sudoku.update_variable(var, value)
            valid = recursive_backtrack(sudoku, test_sudoku)
            if valid == True:
                sudoku.update_variable(var, value)
                return True
        return False

    sudoku_copy = Sudoku(sudoku.export_grid())
    recursive_backtrack(sudoku, sudoku_copy)
    return 
