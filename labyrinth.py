from csp import (
    CSP,
    Constraint,
    BinaryConstraint,
    UnaryConstraint
)

from search import (
    Search,
    State, 
    Labyrinth,
    Position
)

from collections import deque

def permutate(default, k, n): 
    permutations = []
    for i in range(n): 
        tuple = (default,) * n
        tuple[i] = k
        permutations.append(tuple)

    return permutations

def coord_to_index(position: Position, n: int) -> int:
    return position.x * n + position.y

def index_to_coord(index: int, n: int): 
    x = index // n
    y = index % n
    return Position(x, y)

def is_border(x: int, n: int) -> bool:
    pos = index_to_coord(x, n)
    if pos.x == 0 or pos.x == n-1: 
        return True
    elif pos.y == 0 or pos.y == n-1:
        return True
    else:
        return False
    
def is_left_border(x: int, n: int) -> bool: 
    pos = index_to_coord(x, n)
    if pos.y == 0: 
        return True
    else: 
        return False

def is_right_border(x: int, n: int) -> bool: 
    pos = index_to_coord(x, n)
    if pos.y == n-1:
        return True
    else: 
        return False
    
def is_top_border(x: int, n: int) -> bool: 
    pos = index_to_coord(x, n)
    if pos.x == 0: 
        return True
    else: 
        return False

def is_bottom_border(x: int, n: int) -> bool:
    pos = index_to_coord(x, n)
    if pos.x == n-1:
        return True
    else: 
        return False

# Return list of border cells 
def border_cells(cells: list[int], n: int, side: str) -> list[int]:

    checks = {
        "top": is_top_border,
        "bottom": is_bottom_border,
        "left": is_left_border,
        "right": is_right_border,
    }

    return [cell for cell in cells if checks[side](cell, n)]

def create_border_constraints(variables, n: int) -> list[Constraint]: 
    borderConstraints = []
    # for each border variable create a unary constraint 
    for x in variables: 
        if is_top_border(x, n) or is_bottom_border(x, n): 
            borderConstraints.append(UnaryConstraint([x], [(1,)]))
    return borderConstraints

def create_start_constraint(variables, n: int) -> Constraint: 
    start_constraint = Constraint([], [])
    for x in variables: 
        if is_left_border(x, n):
            start_constraint.scope.append(x)
    
    for i in range(start_constraint.arity()): 
        left_border = [1] * start_constraint.arity()
        left_border[i] = 0
        start_constraint.relation.append(tuple(left_border))

    return start_constraint

def create_goal_constraint(variables, n: int) -> Constraint: 
    goal_constraint = Constraint([], [])
    for x in variables: 
            if is_right_border(x, n):
                goal_constraint.scope.append(x)

    for i in range(goal_constraint.arity()): 
            right_border = [1] * goal_constraint.arity()
            right_border[i] = 0
            goal_constraint.relation.append(tuple(right_border))

    return goal_constraint

def create_wall_constraint(variables, num_walls: int): 
    def min_walls(assignment: dict) -> bool: 
            values = [assignment[x] for x in variables]
                
            return values.count(1) + values.count(None) >= num_walls
    
    return Constraint(variables, min_walls)

def create_block_constraints(n: int) -> list[Constraint]:

    def make_block_predicate(square):
        def block_is_valid(assignment):
            return any(assignment[x] in (0, None) for x in square)
        return block_is_valid

    block_constraints = []
    
    for row in range(1, n - 2): 
        for col in range(1, n - 2): 

            square = []

            square.append(coord_to_index(Position(row, col), n))
            square.append(coord_to_index(Position(row + 1, col), n))
            square.append(coord_to_index(Position(row, col + 1), n))
            square.append(coord_to_index(Position(row + 1, col + 1), n))

            predicate = make_block_predicate(square)

            block_constraints.append(Constraint(square, predicate)) 

    return block_constraints

def create_reachability_constraints(variables, n: int): 

# TO-DO: if we pass csp we dont need variables

    def reachable(assignment: dict):  

        temp_assignment = assignment.copy()

        border_variables = [x for x in variables if is_border(x, n)]
        inner_variables = [x for x in variables if x not in border_variables]
        
        # Assign all unassigned fields to 0
        for i in range(len(temp_assignment)):
            if temp_assignment[i] is None: 
                temp_assignment[i] = 0

        # Consider every possible entry points

        entry_points = [] # List of possible entry variables 

        for cell in border_variables: 
            if is_left_border(cell, n) and not is_top_border(cell, n) and not is_bottom_border(cell, n) and temp_assignment[cell] == 0: 
                entry_points.append(cell)

        values = [ temp_assignment[variable] for variable in variables ]

        labyrinth = Labyrinth(values, n)

        # We need to find a SINGLE entry that can reach all required cells 
        for entry in entry_points: 
            reachable = True
            start = index_to_coord(entry, n)
            for cell in inner_variables: 
                # Only open cells in the original assignment have to be reachable 
                if temp_assignment[cell] == 1 or assignment[cell] is None:
                    continue 
                goal = index_to_coord(cell, n)
                reachable = Search.BFS(start, goal, labyrinth)
                if not reachable: 
                    break 
            if reachable: 
                return True

        return False 

    return Constraint(variables, reachable)


def create_solvability_constraint(cells, n):
    # Find all invalid cells
    invalid_cells = border_cells(cells, n, "bottom") + border_cells(cells, n, "top")

    # Find all possible entry variables
    left_border = [ cell for cell in border_cells(cells, n, "left")
    if cell not in invalid_cells ]

    # Find all possible exit variables
    right_border = [ cell for cell in border_cells(cells, n, "right")
    if cell not in invalid_cells ]

    def solvable(partial_assignment: dict):
        # Case 1: No entry or no exit is found 
        if all(partial_assignment[cell] == 1 for cell in left_border) or all(partial_assignment[cell] == 1 for cell in left_border): 
            return False

        # Case 2: Exit and entry are found ( cell is 0 or None )
        
        entry_points = [cell for cell in left_border if partial_assignment[cell] != 1]
        exit_points = [cell for cell in right_border if partial_assignment[cell] != 1]

        # Treat None as open 
        values = [
        0 if partial_assignment[cell] is None else partial_assignment[cell]
        for cell in cells ]
        
        labyrinth = Labyrinth(values, n)

        # Try every possible exit-entry point combination 
        for start in entry_points: 
            for goal in exit_points: 
                search = Search.BFS(start, goal, labyrinth)
                # Return once a valud path was found
                if search: 
                    return True 
        # Fallback if no valid path was found
        return False

    
    return Constraint(cells, solvable)



def createLabCSP(n: int, minimum_walls: int):

    # Variables
    cells = list(range(n*n)) 

    n_cells = len(cells)

    domains = [[0, 1] for _ in range(n_cells)]

    csp = CSP(cells, domains)

    border = [x for x in cells if is_border(x, n)]
    inner = [x for x in cells if x not in border]

    # Create constraints

    # 1st constraint: border is walls
    csp.constraints.extend(create_border_constraints(cells, n))

    #2nd constraint: one opening (start) at the left wall 
    csp.constraints.append(create_start_constraint(cells, n))

    #3rd Constraint: one opening (goal) on the right wall 
    csp.constraints.append(create_goal_constraint(cells, n))

    #4th contstraint at least nWall walls (except border)
    csp.constraints.append(create_wall_constraint(inner, minimum_walls))

    # CONSTRAINT: Every inner 2x2 block has to contain at least one open cell.
    csp.constraints.extend(create_block_constraints(n))
    #block_count = (len(inner) // 2) * 2
    
    #CONSTRAINT: Every INNER block must be reachable from the start 
    csp.constraints.append(create_reachability_constraints(cells, n))

    # CONSTRAINT: Labyrinth must be solvable (a path from entry to exit must exist)
    csp.constraints.append(create_solvability_constraint(cells, n))



    # ISSUE: ASSUMES START AND END ARE ALREADY CHOSEN!!!! 
    #solvable = PredicateConstraint(var, BFS)
    #csp.constraints.extend(solvable)

    return csp 


