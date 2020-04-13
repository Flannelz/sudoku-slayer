# File: printer.py
# Author: Alice Hanigan
# Date: 04/11/2020
#

import value
import constraint

def sudoku_printer(value_grid):
    # Prints a ValueGrid object to the command line

    for i in range(value_grid.get_length()-1):

        line = ""
        divider = ""

        for j in range(value_grid.get_width()-1):

            line += cell_to_str(value_grid.get_value((i,j))) + "|"
            divider += "--"

        print(line + cell_to_str(value_grid.get_value((i, -1))))
        print(divider + "-")

    lastline = ""

    for j in range(value_grid.get_width()-1):

        lastline += cell_to_str(value_grid.get_value((-1,j))) + "|"

    print(lastline + cell_to_str(value_grid.get_value((-1,-1))))

    return

def cell_to_str(val):
    # Converts the contents of a Value object to a String, accounting for possible None values

    if val == None:

        return "."

    else:

        return str(val)
