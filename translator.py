# File: translator.py
# Author: Alice Hanigan
# Date: 04/10/2020
#

import value
import constraint

def translator(value_grid, game_type, rules):
    # Converts the problem into constraints and a grid of starting values
    # Inputs:
    # value_grid is a List<List<Value>> object, containing the initially-known values
    # game_type is a String object, stating the type of problem
    # rules is a List<String> object, each String stating a rule
    #

    constraints = get_type_constraints(game_type)
    constraints += translate_rules(rules)

    return (value_grid, constraints)

def get_type_constraints(game_type):
    # Returns a set of constraints based on the type of game
    # Inputs:
    # game_type is a String object, stating the type of problem

    constraints = []

    # TODO

def translate_rules(rules):
    # Translates the rules into a set of Constraint objects
    # Inputs:
    # rules is a List<String> object, each String stating a rule

    constraints = []
    
    for rule in rules:

        constraints += translate_rule(rule)

    return constraints

def translate_rule(rule):
    # Translates a single rule into a set of Constraint objects
    # Inputs:
    # rule is a String object, stating a rule of the puzzle

    # TODO

    pass
