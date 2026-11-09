from csp import CSP, BinaryConstraint


def is_not_equal(assignment):
    if assignment[1] == assignment[2]: 
        if assignment[1] is None: 
            return True 
        return False
    else: 
        return True 

tabular_constraint = BinaryConstraint([0, 1], [(0,1), (1,0)])

predicate_constraint = BinaryConstraint([1, 2], is_not_equal)

test_constraint = BinaryConstraint([0, 2], [(0,1), (1, 0)])

test_csp = CSP([0, 1, 2], [[0, 1], [0, 1], [0, 1]], [test_constraint, tabular_constraint, predicate_constraint])


# solve csp 
print(test_csp.backtracking_search())