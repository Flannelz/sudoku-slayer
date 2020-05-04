

class Sudoku():
    _members = {}
    _domains = {}
    _neighbors = {}

    def __init__(self, input):
        # TODO: Make variable in size for n < 9
        _Sudoku_Cols = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        _Sudoku_Rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        _Possible_Vals = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        index = 0

        # Variables and Domains
        for prefix in _Sudoku_Rows:
            for suffix in _Sudoku_Cols:
                key = prefix + suffix
                self._members[key] =  input[index]
                if input[index] != 0:
                    self._domains[key] = []
                else:
                    self._domains[key] = _Possible_Vals
                index += 1
        
        # Neighbors
        for cell in self._members:
            cell_row = cell[0]
            cell_col = cell[1]
            # Row Neighbors
            self._neighbors[cell] = [member for member in self._members if member.count(cell_row) == 1 and member != cell]
            # Col Neighbors
            self._neighbors[cell] += [member for member in self._members if member.count(cell_col) == 1 and member != cell]
            
            # Box Neighbors
            if cell_row in ['A', 'B', 'C']:
                row_keys = ['A', 'B', 'C']
            elif cell_row in ['D', 'E', 'F']:
                row_keys = ['D', 'E', 'F']
            elif cell_row in ['G', 'H', 'I']:
                row_keys = ['G', 'H', 'I']
            
            if cell_col in ['1', '2', '3']:
                col_keys = ['1', '2', '3']
            elif cell_col in ['4', '5', '6']:
                col_keys = ['4', '5', '6']
            elif cell_col in ['7', '8', '9']:
                col_keys = ['7', '8', '9']
            
            self._neighbors[cell] += [var for var in self._members if var[0] in row_keys and var[1] in col_keys and var != cell and var not in self._neighbors[cell]]

        #Apply Contraints
        self.apply_constraints()


    # Accessor Functions
    def get_variables(self, cell = None):
        if cell != None:
            return self._members[cell]
        return list(self._members)
    
    # Returns a dictionary mapping cells to their list of possible values
    def get_domains(self, cell = None):
        if cell != None:
            return self._domains[cell]
        return self._domains

    # Returns a dictionary mapping cells to their list of cells related to their constraints
    def get_neighbors(self, cell = None):
        if cell != None:
            return self._neighbors[cell]
        return self._neighbors

    # Returns a list of cell values in the same order as intializer strings
    def export_grid(self):
        grid = []
        for cell in self._members:
            grid.append(self.get_variables(cell))
        return grid


    # Mutator Functions
    def update_variable(self, var, val):
        self._members[var] = val
        self._domains[var] = []
        return
    
    def reset_domain(self, var):
        self._domains[var] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.apply_constraints()

    # Constraint Handling
    def apply_constraints(self):
        for cell in self._members:
            cell_value = self._members[cell]
            if cell_value != 0:
                for neighbor in self._neighbors[cell]:
                    neighbor_values = self._domains[neighbor].copy()
                    if cell_value in neighbor_values:
                        neighbor_values.remove(cell_value)
                        self._domains[neighbor] = neighbor_values
        return

    def constraints_check(self):
        for cell in list(self._neighbors):
            for neighbor in self._neighbors[cell]:
                if self._members[cell] == 0:
                    break
                elif self._members[cell] == self._members[neighbor]:
                    print("member: ", cell, " @ ", self._members[cell], " neighbor: ", neighbor, " @ ", self._members[neighbor])
                    return False
        return True

    # TODO: Global Utility function ( -1 for every constraint broken)

    def goal_check(self):
        for cell in self._members:
            if self._members[cell] == 0:
                return False
        return True
        

    # TODO: Mutate function for GA


# TODO: Get Metrics for each run for matplot lib

#DEAP
# TODO: Determine Fitness of a given state
# TODO: Define a Population
# TODO: Select Parent Members, Crossover to generate Children, Mutate Children, Create new population of children, parents, some "unchosen"
    # TODO: Population Select Roulette, weighted "randomized" choice - for parents
    # TODO: Muatation should not exclude "incorrect" answers - intrinsic backtracking

# Step 1: Create tools
# Step 2: register tools in toolbox
# Step 3: Select Parents
# Step 4: Crossover Parents -> Children
# Step 5: Mutate Children
# Step 6: Fill new population