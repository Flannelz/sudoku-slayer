# File: ga.py
# Authors: Alice Hanigan, Jack Summers
#

import array, random, sudoku, math, itertools
from deap import base, creator, tools

DEBUG = True

def random_grid(grid_size = 9):

    return [random.randint(0, grid_size) for foo in range(grid_size * grid_size)]

def initialize_toolbox(grid_size=9, toolbox = base.Toolbox()):

    # Initialize the fitness method to be a negative score equal to # of constraints broken
    creator.create("MinErrors", base.Fitness, weights=(-10.0, -1.0, -10.0))
    # Initialize the random_solution() method and put it in Toolbox
    # This method generates a Sudoku grid containing (N**2) cells, where N is the specified grid size;
    # Each cell contains a value between 0 and grid_size, with 0 representing an empty cell
    creator.create("Sudoku", sudoku.Sudoku, fitness = creator.MinErrors)
    toolbox.register("attr_int", lambda : random.randint(0, grid_size))
    toolbox.register("sudoku", creator.Sudoku, grid_size = grid_size)

    # Now you can use toolbox.sudoku(input) to get a Sudoku object with a fitness attribute
    # Try this with toolbox.sudoku(random_grid(grid_size)) to easily generate a randomized Sudoku puzzle

    return toolbox

def swap_cells_once(sudoku): # Takes a sudoku puzzle as a list of values, swaps two of their values in place

    i = random.randint(0, len(sudoku)-1)
    j = random.randint(0, len(sudoku)-1)

    temp = sudoku[i]
    sudoku[i] = sudoku[j]
    sudoku[j] = temp

    return sudoku

def default_evaluation(sudo, puzzle = None):

    if sudo.matches_original(puzzle):

        return (sudo.constraints_count(), sudo.empty_count(), 0.0)

    return (sudo.constraints_count(), sudo.empty_count(), 1.0)

def register_evo_functions(
    toolbox,
    evalfunc = default_evaluation, # This method __MUST__ be the evaluation function that takes a guess as a list and returns the number of broken constraints
    matefunc = tools.cxTwoPoint, # This method will be used to get the offspring of two guesses
    mutatefunc = swap_cells_once, # This method will be applied to mutate guesses
    selectfunc = lambda individuals, k : tools.selTournament(individuals, k, tournsize = 4) # This method will be used to select the best guesses in a population
    ):

    toolbox.register("mate", lambda sudo1, sudo2 : [toolbox.sudoku(grid) for grid in matefunc(sudo1.export_grid(), sudo2.export_grid())]) # INPUT : LIST OF INTS, OUTPUT: LIST OF INTS
    toolbox.register("mutate", lambda sudo1 : toolbox.sudoku(mutatefunc(sudo1.export_grid())))  # INPUT : LIST OF INTS, OUTPUT: LIST OF INTS
    toolbox.register("select", selectfunc)
    toolbox.register("evaluate", evalfunc)

    # Functions you can now call:
    # toolbox.mate(a, b) takes two list objects a and b, and returns a list of their crossover children

    return toolbox

def get_random_cell(): # A default function for generating randomized cells, ranging from 0 to 9 (with 0 being an empty cell)

    return random.randint(0, 9)

def default_match_method(parents): # Takes a set of parents, and returns all possible pairs of parents

    parent_sets = []

    for i in range(len(parents)-1):

        for j in range(i+1, len(parents)):

            parent_sets.append([parents[i], parents[j]])

    return parent_sets

def default_recombination(population, parents, children): # Takes the original population, the selected parental candidates, and their offspring, and returns a new population

    length = len(population) # Take the original length of the population
    numChildren = len(children) # And the length of the child population

    if (length > numChildren): # Ensure population stability by selecting individuals from the original population until there are the same number of individuals in the new population

        best = tools.selTournament(population, length - numChildren, tournsize = 4)

        return best + children

    return children

def default_breed_method(parent_set, matefunc): 

    return matefunc(parent_set[0], parent_set[1])

def iterate_one_generation(
    population, # The population of puzzle solutions to be iterated upon DEFAULT POP SIZE = 10
    toolbox, # A toolbox that MUST contain functions "mate", "mutate", "select", and "evaluate"
    k, # The number of parents to be selected for crossover
    puzzle = None,
    match_method = default_match_method, # The method of selecting which parents breed with which, from a pool of selected candidates
    breed_method = default_breed_method, # The method of combining 2 or more parent solutions to make a child solution
    recombine_method = default_recombination # The method of selecting which individuals will ultimately be recombined to make the new population
    ):

    for individual in population:

        individual.fitness.values = toolbox.evaluate(individual, puzzle)

    parents = toolbox.select(population, k)
    parent_sets = match_method(parents)
    children = []

    for parent_set in parent_sets:

        childs = [toolbox.clone(ind) for ind in parent_set]
        childs = breed_method(childs, toolbox.mate)
        children += [toolbox.mutate(child) for child in childs]

    new_population = recombine_method(population, parents, children)

    for p in new_population:

        del p.fitness.values

    return new_population

def run_ga(
    toolbox, # A toolbox that MUST contain functions "mate", "mutate", "select", and "evaluate"
    initial_population, # The initial population
    puzzle = None, # The original puzzle to be solved, if any
    k = 10, # The number of parents to be selected for crossover in each generation
    generations = 1000, # The number of generations to go through before submitting the final population
    match_method = default_match_method, # The method of selecting which parents breed with which, from a pool of selected candidates
    breed_method = default_breed_method, # The method of selecting which parents breed with which, from a pool of selected candidates
    recombine_method = default_recombination # The method of selecting which individuals will ultimately be recombined to make the new population
    ):

    pop = initial_population

    for g in range(generations):

        pop = iterate_one_generation(pop, toolbox, k, puzzle, match_method, breed_method, recombine_method)

        for sudo in pop:

            sudo.fitness.values = toolbox.evaluate(sudo)

            if sudo.goal_check():

                if puzzle == None or sudo.matches_original(puzzle):

                    print("SOLUTION FOUND IN GENERATION:", g)

                    return [sudo]

    return pop

def get_wvalues_avg(pop): # Get the average sum of the weighted fitness values for individuals in this population

    total = 0.0
    
    for individual in pop:

        total += sum(individual.fitness.wvalues)

    return total / len(pop)

def get_wvalues_best(pop): # Get the best sum of the weighted fitness values for individuals in this population

    best = None

    for individual in pop:

        wvalue = sum(individual.fitness.wvalues)

        if best == None:

            best = wvalue

        else:

            best = min(best, wvalue)

    return best

def run_ga_get_data(
    toolbox,
    initial_population,
    puzzle = None,
    k = 10,
    generations = 1000,
    match_method = default_match_method,
    breed_method = default_breed_method,
    recombine_method = default_recombination,
    mode = "WVALUES_AVG"): # this determines the method of data gathering to be performed in this run

    pop = initial_population
    valid_modes = ["WVALUES_AVG", "WVALUES_BEST", "WVALUES_AVG_FINAL", "WVALUES_AVG_LOG10"] # Acceptable modes for data collection

    if mode not in valid_modes: # If the mode passed is not acceptable, default to WVALUES_AVG

        mode = valid_modes[0]

    x_data = []
    y_data = []
    power = 0

    for g in range(generations):

        pop = iterate_one_generation(pop, toolbox, k, puzzle, match_method, breed_method, recombine_method)

        for sudo in pop:

            sudo.fitness.values = toolbox.evaluate(sudo)

            if sudo.goal_check():

                if puzzle == None or sudo.matches_original(puzzle):

                    print("SOLUTION FOUND IN GENERATION:", g)

                    if mode in ["WVALUES_AVG", "WVALUES_AVG_LOG10", "WVALUES_AVG_FINAL"]:

                        x_data.append(g)
                        y_data.append(get_wvalues_avg(pop))

                    if mode in ["WVALUES_BEST", "WVALUES_BEST_LOG10", "WVALUES_BEST_FINAL"]:

                        x_data.append(g)
                        y_data.append(get_wvalues_best(pop))

                    return (pop, x_data, y_data)

        if mode == "WVALUES_AVG": # Data will be the averages of the wvalues fields of each population step

            x_data.append(g)
            y_data.append(get_wvalues_avg(pop))

        if mode == "WVALUES_AVG_LOG10" and (g % 10**power) == 0: # As WVALUES_AVG, but data points are only made for powers of 10

            x_data.append(g)
            y_data.append(get_wvalues_avg(pop))
            power += 1

        if mode == "WVALUES_BEST": # Data will be the best wvalues field among the population at each step

            x_data.append(g)
            y_data.append(get_wvalues_best(pop))

        if mode == "WVALUES_BEST_LOG10" and (g % 10**power) == 0: # As WVALUES_BEST, but data points are only made for powers of 10

            x_data.append(g)
            y_data.append(get_wvalues_best(pop))

    if mode == "WVALUES_AVG_FINAL": # As WVALUES_AVG, but the only data point generated is the final one

        x_data = generations
        y_data = get_wvalues_best(pop)
            
    return (pop, x_data, y_data)

def test_case_1():

    toolbox = initialize_toolbox(4)
    toolbox = register_evo_functions(toolbox)
    grids = [random_grid(4) for foo in range(10)]
    pop = [toolbox.sudoku(grid) for grid in grids]

    for sudo in pop:

        sudo.fitness.values = toolbox.evaluate(sudo)
        print(sudo.export_grid())

    newPop = run_ga(toolbox, pop, k = 2, generations = 1000)

    for sudo in newPop:

        sudo.fitness.values = toolbox.evaluate(sudo)
        print(sudo.export_grid())
        print(sudo.fitness.wvalues)

def test_case_2():

    toolbox = initialize_toolbox(4)
    toolbox = register_evo_functions(toolbox)
    grid = [0,3,0,2,0,0,0,0,0,0,0,0,1,0,2,0]
    grids = [grid for foo in range(10)]
    pop = [toolbox.sudoku(grid) for grid in grids]
    original = toolbox.sudoku(grid, grid_size = 4)

    for sudo in pop:

        sudo.fitness.values = toolbox.evaluate(sudo)
        print(sudo.export_grid())

    newPop = run_ga(toolbox, pop, puzzle = original, k = 2, generations = 10000)

    for sudo in newPop:

        sudo.fitness.values = toolbox.evaluate(sudo)
        print(sudo.export_grid())
        print(sudo.fitness.wvalues)

def test_case_3():

    toolbox = initialize_toolbox(4)
    toolbox = register_evo_functions(toolbox)
    grids = [random_grid(4) for foo in range(10)]
    pop = [toolbox.sudoku(grid) for grid in grids]

    for sudo in pop:

        sudo.fitness.values = toolbox.evaluate(sudo)
        print(sudo.export_grid())

    (newPop, x_data, y_data) = run_ga_get_data(toolbox, pop, k = 2, generations = 1000, mode = "WVALUES_AVG")

    for sudo in newPop:

        sudo.fitness.values = toolbox.evaluate(sudo)
        print(sudo.export_grid())
        print(sudo.fitness.wvalues)

    print(x_data)
    print(y_data)
