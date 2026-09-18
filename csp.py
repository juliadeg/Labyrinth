from collections import deque

class Constraint: 
    def __init__(self, scope: list, relation): 
        self.scope = scope
        self.relation = relation

    # Expects all variables of current constraint scope to be assigned 
    def is_satisfied(self, assignment: dict) -> bool:
        values = tuple(assignment[variable] for variable in self.scope)

        if any(value is None for value in values):
            return #TO-DO Error
        # Predicate Constraint
        if callable(self.relation): 
            return self.relation(values)   
        # Tabular Constraint
        else:   
            return values in self.relation


    # Allows some variables to be unassigned and cheks whether the assignment is consistent so far
    def is_consistent(self, partial_assignment: dict) -> bool: 
        values = tuple(partial_assignment[variable] for variable in self.scope)

        adimissible = False

        if any(value is None for value in values):

            if callable(self.relation): 
                return #TO-DO
            
            else: 
                for allowed_tuple in self.relation: 
                    adimissible = True

                    for i in range(len(values)): 
                        if values[i] is None: 
                            continue 
                        if values[i] != allowed_tuple[i]: 
                            adimissible = False
                            break 

                    if adimissible: 
                        return True
        else: 
            return self.is_satisfied(partial_assignment)

        return adimissible 


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

    # Returns a list of all binary constraints 
    def binary_constraints(self) -> list[BinaryConstraint]:
        return [ constraint for constraint in self.constraints if isinstance(constraint, BinaryConstraint)]

    # Returns a list of constraints the variable is involved for 
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

    def _assigned(self, current_assignment: dict) -> list:
        # TO-DO, simply use unassigned function here
        assigned = []

        for variable in self.variables:
            if variable in current_assignment.keys(): 
                assigned.append(variable)

        return assigned

    
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


        neighbours = self.neighbours(variable)

        assigned_neighbours = [neighbour for neighbour in neighbours if neighbour in self._assigned(assignment)]

        unassigned_neighbours = [neighbour for neighbour in neighbours if neighbour in self._unassigned(assignment)]

        # number of conflicts / ruleouts
        conflicts = 0
        min_conflicts = float('inf') 
        lcv = None

        # neighbour values ruled out
        ruled_out = 0 

        # Assign one of the possible values
        for value in self.domain[variable]: 
        
            assignment[variable] = value 

            #conflicts = 0

            # Check consistency with already assigned variables 


            # Check constraints
            for neighbour in self.neighbours(variable): 
                for constraint in self.constraints_for(neighbour): 
                    # If an already assigned 
                    if not constraint.is_satisfied(assignment):
                        conflicts += 1

            if conflicts < min_conflicts:
                min_conflicts = conflicts
                lcv = value
        
        return lcv
            

        

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
                        if not constraint.is_satisfied({x_var: x_value, y_var: y_value}):
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
    
