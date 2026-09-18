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
    pos = index_to_coord(x)
    if pos.x == 0 or pos.x == n-1: 
        return True
    elif pos.y == 0 or pos.y == n-1:
        return True
    else:
        return False
    
def is_left_border(x: int, n: int) -> bool: 
    pos = index_to_coord(x)
    if pos.y == 0: 
        return True
    else: 
        return False

def is_right_border(x: int, n: int) -> bool: 
    pos = index_to_coord(x)
    if pos.y == n-1:
        return True
    else: 
        return False
    
def is_top_border(x: int, n: int) -> bool: 
    pos = index_to_coord(x)
    if pos.x == 0: 
        return True
    else: 
        return False

def is_bottom_border(x: int, n: int) -> bool:
    pos = index_to_coord(x)
    if pos.x == n-1:
        return True
    else: 
        return False

def create_border_constraints(variables, n: int) -> list[Constraint]: 
    borderConstraints = []
    # for each border variable create a unary constraint 
    for x in variables: 
        if is_top_border(x, n) or is_bottom_border(x, n): 
            borderConstraints.append(UnaryConstraint(x, [1]))
    return borderConstraints

def create_start_constraint(variables, n: int) -> list[Constraint]: 
    start_constraint = Constraint([], [])
    for x in variables: 
        if is_left_border(x, n):
            start_constraint.scope.append(x)
    
    for i in range(start_constraint.arity()): 
        left_border = [1] * start_constraint.arity()
        left_border[i] = 0
        start_constraint.relation.append(tuple(left_border))

    return start_constraint

def create_goal_constraint(variables, n: int) -> list[Constraint]: 
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
    def min_walls(assignment) -> bool: 
            return sum(assignment) >= num_walls
    
    return Constraint(variables, min_walls)

def create_block_constraints(variables, n: int) -> list[Constraint]:

    def block_is_valid(assignment):
        return 0 in assignment

    block_constraints = []
    
    for row in range(n - 1): 
        for col in range(n - 1): 

            square = []

            square.append(coord_to_index(Position(row, col)))
            square.append(coord_to_index(Position(row + 1, col)))
            square.append(coord_to_index(Position(row, col + 1)))
            square.append(coord_to_index(Position(row + 1, col + 1)))

            block_constraints.append(Constraint(square, block_is_valid)) 

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

def createLabCSP(n: int, minimum_walls: int):

    variables = list(range(n*n)) # nxn variables
    n = len(variables)
    domains = [[0, 1] for _ in range(n)]

    csp = CSP(variables, domains)

    border = [x for x in variables if is_border(x)]
    inner = [x for x in variables if x not in border]

    # Create constraints

    # 1st constraint: border is walls
    csp.constr.extend(create_border_constraints(variables, n))

    #2nd constraint: one opening (start) at the left wall 
    csp.constr.extend(create_start_constraint(variables, n))

    #3rd Constraint: one opening (goal) on the right wall 
    csp.constr.extend(create_goal_constraint(variables, n))

    #4th contstraint at least nWall walls (except border)
    csp.constr.extend(create_wall_constraint(inner, minimum_walls))

    # CONSTRAINT: Every inner 2x2 block has to contain at least one open cell.
    csp.constr.extend(create_block_constraints(inner, n))
    #block_count = (len(inner) // 2) * 2
    
    #CONSTRAINT: Every INNER block must be reachable from the start 
    csp.constr.extend(create_reachability_constraints(variables, n))
    







    #th constraint: must be solvavble

    # ISSUE: ASSUMES START AND END ARE ALREADY CHOSEN!!!! 
    solvable = PredicateConstraint(var, BFS)
    csp.constr.extend(solvable)

    return csp 


