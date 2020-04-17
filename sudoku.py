

class Sudoku():
    _members = {}
    _domains = {}
    _neighbors = {}

    def __init__(self, input):
        _Sudoku_Cols = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        _Sudoku_Rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        _Possible_Vals = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        index = 0

        # Variables and Domains
        for prefix in _Sudoku_Rows:
            for suffix in _Sudoku_Cols:
                key = prefix + suffix
                self._members[key] =  input[index]
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
            
            self._neighbors[cell] += [var for var in self._members if var[0] in row_keys and var[1] in col_keys and var != cell]

        #Apply Contraints
        self.apply_constraints()


    # Accessor Functions
    def get_variables(self, cell = None):
        if cell != None:
            return self._members[cell]
        return list(self._members)
    
    def get_domains(self, cell = None):
        if cell != None:
            return self._domains[cell]
        return self._domains

    def get_neighbors(self, cell = None):
        if cell != None:
            return self._neighbors[cell]
        return self._neighbors

    def export_grid(self):
        grid = []
        for cell in self._members:
            grid.append([self.get_variables(cell)])
        return grid


    # Constraint Handling
    def apply_constraints(self):
        for cell in self._members:
            cell_value = self._members[cell]
            if cell_value != 0:
                for neighbor in self._neighbors[cell]:
                    self._domains[neighbor] = self._domains[neighbor].remove(cell_value)

    def constraints_check(self):
        for cell in list(self._neighbors):
            for neighbor in self._neighbors[cell]:
                if self._members[cell] != 0 and self._members[cell] == self._members[neighbor]:
                    return False
        return True
