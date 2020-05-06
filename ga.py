# File: ga.py
# Authors: Alice Hanigan, Jack Summers
#

import array, random, sudoku, math, itertools
from deap import base, creator, tools

DEBUG = False

def random_grid(grid_size = 9):

    return [random.randint(0, grid_size) for foo in range(grid_size * grid_size)]

def initialize_toolbox(grid_size=9, toolbox = base.Toolbox()):

    # Initialize the fitness method to be a negative score equal to # of constraints broken
    creator.create("MinErrors", base.Fitness, weights=(-1.0,))
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

def default_evaluation(sudo):

    return (sudo.constraints_count(),)

def register_evo_functions(
    toolbox,
    evalfunc = default_evaluation, # This method __MUST__ be the evaluation function that takes a guess as a list and returns the number of broken constraints
    matefunc = tools.cxTwoPoint, # This method will be used to get the offspring of two guesses
    mutatefunc = swap_cells_once, # This method will be applied to mutate guesses
    selectfunc = tools.selRoulette # This method will be used to select the best guesses in a population
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

    return parents + children # This default method simply chooses the parents and the children, ignoring any unselected candidates

def default_breed_method(parent_set, matefunc): # Takes a set of parents [P1, ..., Pn] and a mate function, and returns the result of replacing P1 and P2 with their child until the only element in the list is a single child

    if len(parent_set) == 1:

        return parent_set[0]

    children = matefunc(parent_set[0], parent_set[1])
    new_parent_set = children + parent_set[3:]

    return default_breed_method(new_parent_set, matefunc)

def iterate_one_generation(
    population, # The population of puzzle solutions to be iterated upon DEFAULT POP SIZE = 10
    toolbox, # A toolbox that MUST contain functions "mate", "mutate", "select", and "evaluate"
    k, # The number of parents to be selected for crossover
    match_method = default_match_method, # The method of selecting which parents breed with which, from a pool of selected candidates
    breed_method = default_breed_method, # The method of combining 2 or more parent solutions to make a child solution
    recombine_method = default_recombination # The method of selecting which individuals will ultimately be recombined to make the new population
    ):

    for individual in population:

        individual.fitness.values = toolbox.evaluate(individual)

    parents = toolbox.select(population, k)
    parent_sets = match_method(parents)
    children = []

    for parent_set in parent_sets:

        child = breed_method(parent_set, toolbox.mate)
        children.append(toolbox.mutate(child))

    new_population = recombine_method(population, parents, children)

    return new_population

def run_ga(
    puzzle, # A puzzle represented as a tuple (grid, constraints), where grid is a list of N**2 cells, and constraints is the list of all constraints on this puzzle
    toolbox, # A toolbox that MUST contain functions "mate", "mutate", "select", and "evaluate"
    initial_population, # The initial population
    k = 10, # The number of parents to be selected for crossover in each generation
    generations = 1000, # The number of generations to go through before submitting the final population
    breed_method = default_breed_method, # The method of selecting which parents breed with which, from a pool of selected candidates
    recombine_method = default_recombination # The method of selecting which individuals will ultimately be recombined to make the new population
    ):

    pop = initial_population

    for g in range(generations):

        pop = iterate_one_generation(pop, toolbox, k, breed_method, recombine_method)

    return pop
