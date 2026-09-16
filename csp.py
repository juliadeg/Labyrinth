from collections import deque

class Constraint: 
    def __init__(self, scope: list, relation): 
        self.scope = scope
        self.relation = relation

    def is_satisfied(self, assignment: tuple) -> bool:
        # Predicate Constraint
        if callable(self.relation): 
            return self.relation(assignment)   
        # Tabular Constraint
        else:   
            return assignment in self.relation

    def arity(self):
        return len(self.scope)

class UnaryConstraint(Constraint): 
    pass

class BinaryConstraint(Constraint): 
    pass

class CSP: 
    def __init__(self, variables: list, domain: list[list], constraints: list[Constraint] | None = None): 
        self.variables = variables
        self.domain = domain 
        self.constraints = [] if constraints is None else constraints

    def binary_constraints(self) -> list[BinaryConstraint]:
        return [ constraint for constraint in self.constraints if isinstance(constraint, BinaryConstraint)]

    def constraints_for(self, variable) -> list[Constraint]: 
        variable_constraints = []
        for constraint in self.constraints:
            if variable in constraint.scope: 
                variable_constraints.append(constraint)
        return variable_constraints

    # Optional argument: Only show binary neighbpurs (for ac3)
    def neighbours(self, variable, arity: int | None = None ) -> list: 
        neighbours = set()
        variable_constraints = self.constraints_for(variable)

        if arity is not None: 
            for constraint in variable_constraints: 
                if constraint.arity() == arity: 
                    neighbours.update(constraint.scope)
        else:  
            for constraint in variable_constraints: 
                neighbours.update(constraint.scope)

        neighbours.discard(variable) # Remove the variable whos neighbours we are looking for 

        return list(neighbours)
    
    def binary_constraints_involving(self, x, y) -> list[Constraint]: 
            matching_constraints = set()
    
            for constraint in self.constraints:
                if constraint.arity() == 2: 
                    if x in constraint.scope and y in constraint.scope: 
                        matching_constraints.add(constraint)
        
            return list(matching_constraints)

    def _prune_domain(self, variable, value):
        self.domain[variable].remove(value)

    def _unassigned(self, current_assignment: dict) -> list:

        unassigned = []

        for variable in self.variables:
            if variable not in current_assignment.keys(): 
                unassigned.append(variable)

        return unassigned


    
    
    def degree(self, variable: int, current_assignment: dict):

        degree = 0 

        current_unassigned = self._unassigned(current_assignment)

        for constraint in self.constraints:
            # variables scope contains at least one other unassigned variable

            # True if the constraint contains at least one other unassigned variable.
            has_other_unassigned = any(    
                other_var in current_unassigned and other_var != variable
                for other_var in constraint.scope
            )
 
            if  variable in constraint.scope and has_other_unassigned: 
                degree += 1

        return degree 


    def _mrv():
        
        None

    def _lcv(self, variable: int, assignment: dict): 

        # number of conflicts / ruleouts

        conflicts = []

        # Assign one of the possible values
        for value in self.domain[variable]: 
            assignment[variable] = value 

        # Check constraints
        for variable in self.neighbours(variable): 
            

        

        None

    def _degree_heuristic(self, current_assignment: dict) -> int: 

        unassigned_variables = self._unassigned(current_assignment)
        highest_degree = 0
        highest_degree_var = unassigned_variables[0]

        for x in unassigned_variables: 
            current_degree = self.degree(x, current_assignment)
            if current_degree > highest_degree: 
                highest_degree = current_degree
                highest_degree_var = x

        return highest_degree_var 


    def _ac3(self) -> bool: 

        # Case of empty domain
        if any(not self.domain[var] for var in self.variables):
            return False

        def _revise(x_var, y_var) -> bool: 

            revised = False
        
            binary_constraints = self.binary_constraints_involving(x_var, y_var)

            for x_value in self.domain[x_var].copy(): 
                y_value_found = False

                for y_value in self.domain[y_var]: 
                    y_value_found = True

                    for constraint in binary_constraints: 
                        if constraint.scope[0] == x_var:
                            values = (x_value, y_value)
                        else:
                            values = (y_value, x_value)

                        if not constraint.is_satisfied(values):
                            y_value_found = False
                            break 

                    if y_value_found:
                        break 

                if not y_value_found: 
                    self._prune_domain(x_var, x_value)
                    revised = True

            return revised

        queue = deque()

        # Initialize queue with all arcs in the CSP 
        arcs = set()
        all_binary_constraints = self.binary_constraints()

        for constraint in all_binary_constraints: 
            x, y = constraint.scope
            arcs.add((x,y))
            arcs.add((y,x))

        queue.extend(arcs)

        while queue: 

            x_var, y_var = queue.popleft()

            x_domain = self.domain[x_var]
            y_domain = self.domain[y_var]

            if _revise(x_var, y_var): 
                if not x_domain:
                    return False
                for k in self.neighbours(x_var):
                    if k == y_var:
                        continue
                    queue.append((k, x_var))
        return True


    
    def backtracking_search(self):
        assignment = dict()

        # Pick variable:
        variable = self._degree_heuristic(assignment)

        # Pick value:
        value = None

        return assignment
    
