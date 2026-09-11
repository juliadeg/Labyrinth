from csp import (
    CSP,
    Constraint,
    BinaryConstraint,
    PredicateConstraint,
    TableConstraint,
    index_to_cord,
)

class Position: 
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_tuple(self) -> tuple: 
        return (self.x,self.y)
    
    def __eq__(self, other):
        if not isinstance(other, Position):
            return NotImplemented
        return (self.x == other.x and self.y == other.y)

def coord_to_index(position: Position, n: int):
    return position.x * n + position.y

def index_to_coord(index: int, n: int): 
    x = index // n
    y = index % n
    return Position(x, y)


def is_border(x: int, n: int) -> bool:
    pos = index_to_cord(x)
    if pos.x == 0 or pos.x == n-1: 
        return True
    elif pos.y == 0 or pos.y == n-1:
        return True
    else:
        return False
    
def is_left_border(x: int, n: int) -> bool: 
    pos = index_to_cord(x)
    if pos.y == 0: 
        return True
    else: 
        return False

def is_right_border(x: int, n: int) -> bool: 
    pos = index_to_cord(x)
    if pos.y == n-1:
        return True
    else: 
        return False
    
def is_top_border(x: int, n: int) -> bool: 
    pos = index_to_cord(x)
    if pos.x == 0: 
        return True
    else: 
        return False

def is_bottom_border(x: int, n: int) -> bool:
    pos = index_to_cord(x)
    if pos.x == n-1:
        return True
    else: 
        return False


def createLabCSP(n: int):

    from labyrinth_search import BFS

    var = list(range(n*n)) # nxn variables

    nVar = len(var)

    domains = [[0, 1] for _ in range(n)]

    csp = CSP(var, domains)

    # Create constraints

    # 1st constraint: border is walls

    borderConstraints = []
    # for each border variable create a unary constraint 
    for x in var: 
        if is_top_border(x, n) or is_bottom_border(x, n): 
            borderConstraints.append(UnaryConstr(x, [1]))

    csp.constr.extend(borderConstraints)

    #2nd constraint: one opening (start) at the left wall 
    startConstraint = Constraint([], [])
    for x in var: 
        if is_left_border(x, n):
            startConstraint.scope.append(x)

    for i in range(startConstraint.arity()): 
        leftBorder = [1] * startConstraint.arity()
        leftBorder[i] = 0
        startConstraint.relation.append(tuple(leftBorder))

    csp.constr.extend(startConstraint)

    #3rd Constraint: one opening (goal) on the right wall 
    goalConstraint = Constraint([], [])
    for x in var: 
            if is_right_border(x, n):
                goalConstraint.scope.append(x)

    for i in range(goalConstraint.arity()): 
            rightBorder = [1] * goalConstraint.arity()
            rightBorder[i] = 0
            goalConstraint.relation.append(tuple(rightBorder))

    csp.constr.extend(goalConstraint)

    #4th contstraint at least nWall walls (except border)

    border = [x for x in var if is_border(x)]
    inner = var - border

    def minWall(inner: list, nWall: int) -> bool: 
        return sum(inner) >= nWall

    wallsConstraint = PredicateConstraint(inner, minWall)

    csp.constr.extend(wallsConstraint)

    #5th constraint: must be solvavble

    # ISSUE: ASSUMES START AND END ARE ALREADY CHOSEN!!!! 
    solvable = PredicateConstraint(var, BFS)
    csp.constr.extend(solvable)

    return csp 



