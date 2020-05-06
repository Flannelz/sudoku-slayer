from deap import base, creator, tools

DEBUG = False

class Sudoku():

    # NOTE: I moved the class variable initialization to within the __init__ method
    # The way it was implemented, these were *global* variables, and would update across all Sudoku objects when one updated
    # Now, these should be unique to each Sudoku object

    def __init__(self, inp, grid_size = 9): # Changed "input" to "inp", to avoid any mix-ups in using a keyword
        # TODO: Make variable in size for n < 9
        _Sudoku_Cols = ['1', '2', '3', '4', '5', '6', '7', '8', '9'][:grid_size]
        _Sudoku_Rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'][:grid_size]
        _Possible_Vals = [1, 2, 3, 4, 5, 6, 7, 8, 9][:grid_size]
        self._grid_size = grid_size
        self._members = {}
        self._domains = {}
        self._neighbors = {}
        index = 0

        # Variables and Domains
        for prefix in _Sudoku_Rows:
            for suffix in _Sudoku_Cols:
                key = prefix + suffix
                self._members[key] =  inp[index]
                if inp[index] != 0:
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

            if grid_size == 9:
                
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

            if grid_size == 6:

                if cell_row in ['A', 'B']:
                    row_keys = ['A', 'B']
                elif cell_row in ['C', 'D']:
                    row_keys = ['C', 'D']
                elif cell_row in ['E', 'F']:
                    row_keys = ['E', 'F']
            
                if cell_col in ['1', '2', '3']:
                    col_keys = ['1', '2', '3']
                elif cell_col in ['4', '5', '6']:
                    col_keys = ['4', '5', '6']

            if grid_size == 4:

                if cell_row in ['A', 'B']:
                    row_keys = ['A', 'B']
                elif cell_row in ['C', 'D']:
                    row_keys = ['C', 'D']

                if cell_col in ['1', '2']:
                    col_keys = ['1', '2']
                elif cell_col in ['3', '4']:
                    col_keys = ['3', '4']
            
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
        self._domains[var] = range(1, self._grid_size+1)
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

    def constraints_count(self):

        broken = 0

        for cell in list(self._neighbors):
            if DEBUG: print("Cell:", cell)
            for neighbor in self._neighbors[cell]:
                if self._members[cell] == 0:
                    break
                elif self._members[cell] == self._members[neighbor]:
                    if DEBUG: print("Neighbor:", neighbor)
                    broken += 1

        return broken

    def empty_count(self):

        empty = 0

        for cell in self.export_grid():

            if cell == 0:

                empty += 1

        return empty

    def goal_check(self):
        for cell in self._members:
            if self._members[cell] == 0:
                return False
        return (self.constraints_count() == 0)

    def matches_original(self, original):

        if original == None:

            return True

        self_grid = self.export_grid()
        original_grid = original.export_grid()

        if len(self_grid) != len(original_grid):

            return False

        for i in range(len(self_grid)):

            if original_grid[i] != 0 and self_grid[i] != original_grid[i]:

                return False

        return True

def print_sudoku(sudo, grid_size = None):

    grid = sudo.export_grid()
    if grid_size == None: grid_size = int(len(grid) ** 0.5)

    print_grid(grid, grid_size)

def print_grid(grid, grid_size):

    for i in range(grid_size):

        row = grid[i*grid_size:i*grid_size+grid_size]
        output = ""

        for j in range(grid_size):

            cell = row[j]

            if cell == 0:

                output += " "

            else:

                output += str(cell)

            if j < grid_size-1:

                output += " | "

        print(output)

        if i < grid_size-1:

            print("".join(["-" for foo in range((grid_size * 4) - 1)]))

    return


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
