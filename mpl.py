# File: mpl.py
# Authors: Alice Hanigan, Jack Summers
#

import sudoku, ga
from deap import base, creator, tools
from matplotlib import pyplot

def plot_data(x_data, y_data):

    pyplot.plot(x_data, y_data)

    return

def run_ga_plot_data(
    toolbox,
    initial_population,
    puzzle = None, 
    k = 10,
    generations = 1000,
    match_method = ga.default_match_method,
    breed_method = ga.default_breed_method,
    recombine_method = ga.default_recombination,
    mode = "WVALUES_AVG"): # this determines the method of data gathering to be performed in this run

    (pop, x_data, y_data) = ga.run_ga_get_data(toolbox, initial_population, puzzle, k, generations, match_method, breed_method, recombine_method, mode)

    plot_data(x_data, y_data)

    return

def test_case_1():

    toolbox = ga.initialize_toolbox(4)
    toolbox = ga.register_evo_functions(toolbox)
    grids = [ga.random_grid(4) for foo in range(10)]
    pop = [toolbox.sudoku(grid) for grid in grids]

    run_ga_plot_data(toolbox, pop, k = 2, generations = 1000, mode = "WVALUES_AVG")
    pyplot.show()

def test_case_2():

    
    toolbox = ga.initialize_toolbox(4)
    toolbox = ga.register_evo_functions(toolbox)
    grids = [ga.random_grid(4) for foo in range(10)]
    pop = [toolbox.sudoku(grid) for grid in grids]

    run_ga_plot_data(toolbox, pop, k = 2, generations = 10000, mode = "WVALUES_AVG")
    pyplot.show()

def test_case_3():

    
    toolbox = ga.initialize_toolbox(4)
    toolbox = ga.register_evo_functions(toolbox)
    grids = [ga.random_grid(4) for foo in range(10)]
    pop = [toolbox.sudoku(grid) for grid in grids]

    run_ga_plot_data(toolbox, pop, k = 2, generations = 10000, mode = "WVALUES_BEST")
    pyplot.show()
