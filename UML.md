# UML for CSP 


```mermaid
classDiagram
    class Position {
        int x
        int y

        to_tuple() tuple
        __eq__(other: Position) bool
    }

    class Constraint {
        list~~ scope
        relation

        is_satisfied(assignment: tuple) bool
        arity() int
    }
    
    class UnaryConstraint{

        }

    Constraint <|-- UnaryConstraint

    class BinaryConstraint{
        
    }

    Constraint <|-- BinaryConstraint

    class CSP {
        variables : list 
        domain : list~list~
        constraints: list~Constraint~ = None

        binary_constraints() list~BinaryConstraint~
        
        neighbours(variable) list
        
        binary_constraints_involving(x, y) list~Constraint~

        constraints_for(variable) list~Constraint~

        degree(variable, current_assignment: dict) int
        
        _prune_domain(variable, values: list)

        _unassigned(current_assignment: dict) list 

        _least_constraining_value()

        backtracking_search()

        _mrv()

        _degree_heuristic(current_assignment: dict)

        _ac3() bool
    }

```


# UML for Searching 

```mermaid
classDiagram
    class Labyrinth {
        list~list~int~~ grid

        is_wall(pos: Position) bool

        is_insid(pos: Position) bool  

    }
```
