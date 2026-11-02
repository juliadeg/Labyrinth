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
            return self.relation(assignment)   
        # Tabular Constraint
        else:   
            return values in self.relation


    # Allows some variables to be unassigned and cheks whether the assignment is consistent so far
    def is_consistent(self, partial_assignment: dict) -> bool: 
        values = tuple(partial_assignment[variable] for variable in self.scope)

        adimissible = False

        if any(value is None for value in values):

            if callable(self.relation): 
                # Partial assignments have to be handled inside the predicate constraints  
                return self.relation(partial_assignment)
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

    # Check consistency with constraints involving selected variables or consistency across all constraints 
    def is_consistent(self, assignment: dict, variables: list | None = None) -> bool: 
        constraints = []
        if variables is None:   
            for constraint in self.constraints: 
                if not constraint.is_consistent(assignment): 
                    return False 
        else: 
            for variable in variables: 
                constraints.extend(self.constraints_for(variable))

            # Remove duplicates
            constraints = list(set(constraints))

            for constraint in constraints: 
                if not constraint.is_consistent(assignment): 
                    return False 
        return True 

    
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
    
    def binary_constraints_for(self, x, y) -> list[Constraint]: 
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
            if current_assignment[variable] is None: 
                unassigned.append(variable)

        return unassigned

    def _assigned(self, current_assignment: dict) -> list:

        assigned = []

        for variable in self.variables:
            if current_assignment[variable] is not None:
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

        lcv = None 

        temp_assignment = assignment.copy()

        neighbours = self.neighbours(variable)
        unassigned_neighbours = [neighbour for neighbour in neighbours if neighbour in self._unassigned(assignment)]

        # Store the number of values ruled out for each unassigned variable 
        conflict_list = [0] * len(unassigned_neighbours)

        min_conflict_list = None

        # Assign all possible values for our variable 
        for value in self.domain[variable]: 
    
            temp_assignment[variable] = value 

            # Check that the value is consistent with current assignment, if not try the next value
            if not self.is_consistent(temp_assignment, variables = [variable]): 
                continue  
                
            # After valid value is found, iterate over all unassigned neighbours and check what values are ruled out 

            for i, neighbour in enumerate(unassigned_neighbours): 
                # Try all possible values for the neighbour
                for neighbour_value in self.domain[neighbour]:
                    temp_assignment[neighbour] = neighbour_value 
                    # Check consistency and add conflict if inconsistent
                    if not self.is_consistent(temp_assignment, variables = [neighbour]):
                        conflict_list[i] += 1 

                # Reset assignment
                temp_assignment[neighbour] = None 
                
            # Take the sum of all condlicts and store the minimal sum and the corresponding value (lcv)
            if min_conflict_list is None or sum(conflict_list) <= sum(min_conflict_list):
                min_conflict_list = conflict_list.copy()
                lcv = value

                
            # Reset conflict list for each value candidate 
            conflict_list = [0] * len(unassigned_neighbours)

        return lcv


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
        
            binary_constraints = self.binary_constraints_for(x_var, y_var)

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
                for k in self.neighbours(x_var, 2):
                    if k == y_var:
                        continue
                    queue.append((k, x_var))
        return True

    def forward_checking(self, partial_assignment: dict, variable): 

        constraints = self.constraints_for(variable)

        for constraint in constraints: 
            unassigned = self._unassigned(partial_assignment)
            for unassigned_var in unassigned: 
                values = self.domain[unassigned_var]
                for value in values: 
                    partial_assignment[unassigned_var] = value

                    # Remove value if it causes an inconsietency
                    if not self.is_consistent(partial_assignment): 
                        self.domain[unassigned_var].remove(value)

                    # Terminate if domain becomes empty i.e. no consistent assignment is found
                    if not self.domain[unassigned_var]: 
                        return False

        return True 

    def backtracking_search(self): 

        # initialize empty assignment 
        assignment = dict()
        for variable in self.variables: 
            assignment[variable] = None

        return self.backtrack(assignment)
    
    def backtrack(self, assignment):

        # If assignment is complete return assignment
        if all(value is not None for value in assignment.values()): 
            if self.is_consistent(assignment):
                return assignment 
            return False
        
        # Pick variabl using degree heuristic:
        variable = self._degree_heuristic(assignment) 

        # Order domain values based on lcv 
        sorted_values = []

        domain_copy = self.domain[variable].copy()

        while domain_copy:
            lcv = self._lcv(variable, assignment)
            if lcv not in domain_copy:
                break
            sorted_values.append(lcv)
            domain_copy.remove(lcv)

        # Try assigning ordered values 
        
        for value in sorted_values: 
            if self.is_consistent(assignment | {variable: value}): # temporarily assign the value
                assignment[variable] = value 

                # Safe domains before inference to restore in case of failure
                saved_domains = [domain.copy() for domain in self.domain]

                # Inference
                inferences = self.forward_checking(assignment, variable)
                if inferences: 
                    # add inferences to csp (already done i think)
                    result = self.backtrack(assignment)
                    if result is not False: 
                        return result 
                # Remove inferences from CSP 
                self.domain = saved_domains
                # Remove incorrect assignment
                assignment[variable] = None 
        return False 




        # Check consistency 
        self.is_consistent()



        return assignment
    
