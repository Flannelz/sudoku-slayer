# File: value.py
# Author: Alice Hanigan
# Date: 04/10/2020
#

import copy

class Value:
    # A class for a "cell" of a Sudoku puzzle
    # Fields:
    # value: a representation of the *known* value of this cell (set to None if it is unknown)
    # guesses: the set of *all* remaining possible values of this cell (it is *crucial* that this is initialized to the domain of the variable)

    def __init__(self, val=None, guesses=[i+1 for i in range(9)]):

        self.value = val
        self.guesses = guesses

    def to_string(self):

        if (self.get_value() == None):

            return "."

        return str(self.value)

    def get_value(self):

        return self.value

    def get_guesses(self):

        return self.guesses

    def set_value(self, val):

        self.value = val

    def eliminate(self, guesses):
        # Removes *all* of the guesses listed from the object's set of possible values

        for guess in guesses:

            self.eliminate(guess)

    def eliminate(self, guess):
        # Removes one guess from the list of possible values
        # If this leaves exactly 1 possible value, the Value object will automatically update its value field to this

        self.guesses.remove(guess)

        if len(self.get_guesses()) == 1:

            self.set_value(self.get_guesses()[0])

class ValueGrid:
    # A class for a Sudoku grid (or a similar puzzle)
    # Fields:
    # values: an NxN matrix of Value objects

    def __init__(self, vals):

        self.values = vals

    def __init__(self, n):

        domain = [i+1 for i in range(n)]

        self.values = [[Value(None, domain) for i in range(n)] for j in range(n)]

    def get_values(self):

        return self.values

    def get_guesses(self, address):

        return self.values[address[0]][address[1]].get_guesses()

    def get_value(self, address):

        return self.values[address[0]][address[1]].get_value()

    def set_value(self, address, val):

        self.values[address[0]][address[1]].set_value(val)

    def eliminate(self, address, guesses):
        # Removes all the listed guesses from the addressed Value object's guesses field

        self.values[address[0]][address[1]].eliminate(guesses)

    def get_length(self):
        

        return len(self.values)
    
    def clone(self):
        # Creates a deep copy (all *values* are copied via recursion, no pointers are duplicated)

        return copy.deepcopy(self)

    def guess(self, address, guess):
        # Create a copy of the ValueGrid, with a specific guess made from the addressed Value object's set of possible values

        clone = self.clone()
        clone.set_value(address, guess)

        return clone

    def get_options(self):
        # Returns a list of *all* possible next guesses
        # Each guess is represented as a tuple (addr, guess)
        # where addr is a tuple of the Value's index in the ValueGrid
        # and guess is the value we are testing for it

        options = []
        vals = self.get_values()

        for i in range(len(vals)):

            for j in range(len(vals[0])):

                val = self.get_value((i, j))
                guesses = self.get_guesses((i,j))

                if len(guesses) > 1:

                    for guess in guesses:

                        options.append(((i, j), guess))

        return options
