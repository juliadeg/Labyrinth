


## Labyrinth as a CSP

- Goal: Given a parameter size $n$ and a minimum number of walls $nWalls$ (excluding the border), find a solvable labyrinth constellation with an entry and an exist. 

Problem Formulation as CSP: 

$$
CSP = \langle \mathcal{X}, \mathcal{D}, \mathcal{C} \rangle
$$

#### Variables $\mathcal{X}$

For a $n \times n$ grid we create $n \times n$ variables, each denoting one cell in the labyrinth grid:

$$
\mathcal{X} = \{X_0, X_1, X_2, \ldots, X_{n \times n - 1}\}
$$

#### Domains $\mathcal{D}$

We denote a wall in the labyrinth as $1$ and an empty cell as $0$. Every variable can either be a wall or a empty cell:

$$
\mathcal{D} = \{D_0, D_1, D_2, \ldots, D_{n \times n - 1}\}
$$
where

$$
D_0 = D_1 = D_2 = \dots = D_{n \times n - 1} = \{0,1\}
$$

#### Constraints $\mathcal{D}$

Each Constraint can be defined as: 

$$
C =
\begin{cases}
Scope(C) & \subseteq \mathcal{X}  \\
Relation(C) & \subseteq \prod_{x \in Sc(C)}^{} D_x
\end{cases}
$$

We differentiate between Tabular Constraints and Predicate Constraints. 
##### Tabular Constraints
The Relation, as per definition, is expressed as a set of allowed tuples for the constraint.
##### Predicate Constraints
The Relation is expressed as a function. 

Furtherly constraints can be differentiated based on their *arity*. The arity of a constraint is the number of variables involved in the constraint i.e. the cardinality of its scope (Unary Constraints, Binary Constraints, ..., n-ary Constraints). For CSP-solvers it is desirable to keep the arity small. Any n-ary CSP can be converted into a binary constraint. 

For the labyrinth finder we define the following constraints:

##### Constraint 1: The top and bottom border of the labyrinth are all walls
Instead of expressing a single $2n$-ary constraint involving all top and bottom border variables, we can express $2n$ unary constraints. 

First we find all necessary border variables:

$$
\mathcal{X}_{TBborder} = \{X_{B,0}, X_{B,1}, \dots, X_{B,2n}\} \subseteq \mathcal{X}
$$

For each Border variable $X_{B,i}$ we define the following constraint: 

$$
C_{1, i} =
\begin{cases}
Scope(C_{1, i}) = \{X_{B,i}\}  \\
Relation(C_{1, i}) = \{(1)\}
\end{cases}
$$

- Unary Constraint
- Tabular Constraint

##### Constraint 2: The left border is all wally except exactly one opening (start).
Once again we define all left border variables as follows: 

$$
\mathcal{X}_{leftborder} = \{X_{B,0}, X_{B,1}, \dots, X_{B,2n}\} \subseteq \mathcal{X}
$$

Due to the dependence within the variables, we will define a single $2n$-ary constraint.

$$
C_2 =
\begin{cases}
Scope(C_2) = \{X_{B,0}, X_{B,1}, \dots, X_{B,2n}\}  \\
Relation(C_2) = \{(0,1,1, ...), (1, 0, 1, ...), (1, 1, 0, ...), \dots\}
\end{cases}
$$

For the relation, we have exactly $n$ possibilities to distribute one opening among n cells. More precisely this can be expressed as follows: 

$$
Relation(C_2) = \left\{(x_1,\ldots,x_n)\mid \exists j\in\{1,\ldots,n\}:\ x_j=k,\ x_i=0\text{ for all }i\ne j\right\}
$$

- $2n$-ary Constraint
- Tabular Constraint

##### Constraint 3: The right border is all wall except exactly one opening (goal).

We define this constraint equivalently to constraint 2: 

$$
\mathcal{X}_{rightborder} = \{X_{B,0}, X_{B,1}, \dots, X_{B,2n}\} \subseteq \mathcal{X}
$$

$$
C_3 =
\begin{cases}
Scope(C_2) = \{X_{B,0}, X_{B,1}, \dots, X_{B,2n}\}  \\
Relation(C_2) = \{(0,1,1, ...), (1, 0, 1, ...), (1, 1, 0, ...), \dots\}
\end{cases}
$$
or alternatively:
$$
Relation(C_3) = \left\{(x_1,\ldots,x_n)\mid \exists j\in\{1,\ldots,n\}:\ x_j=k,\ x_i=0\text{ for all }i\ne j\right\}
$$

- $2n$-ary Constraint
- Tabular Constraint

##### Constraint 4: Every overlapping 2x2 block has to contain at least one open cell. 

The purpose of this constraint is to avoid big chunks of walls inside our labyrinth.

For a $n \times n$ labyrinth a $2 \times 2$ block is made of the following variables.

For every variable $X_{i,j}$ where $i,j \in \{1, \ldots, n-1\}$ we have $X_{i,j}, X_{i+1,j}, X_{i,j+1}, X_{i+1,j+1}$.

In total we will have $(n-1) \times (n-1)$ such blocks. For each block we define the 4-ary constraint:

$$
C_{4,i,j} =
\begin{cases}
Scope(C_{4,i,j}) = \{X_{i,j}, X_{i+1,j}, X_{i,j+1}, X_{i+1,j+1}\} \\
Relation(C_{4,i,j}) = \operatorname{block\_is\_valid}(X_{i,j}, X_{i+1,j}, X_{i,j+1}, X_{i+1,j+1})
\end{cases}
$$

# CHANGE TO Putting PARTIAL ASSIGNMENT INTO PARAMETER

Where we define the `block_is_valid` function as follows:

$$
\operatorname{block\_is\_valid}(X_{i,j}, X_{i+1,j}, X_{i,j+1}, X_{i+1,j+1}) =
\begin{cases}
\mathrm{False} & \text{if the } 2 \times 2 \text{ block contains only 1s}, \\
\mathrm{True} & \text{otherwise}.
\end{cases}
$$

This leaves us with $(n-1) \times (n-1)$ 4-ary constraints.

Note that this function treats `None` fields as open fields. So an unassigned $2 \times 2$ block for example would still be valid.

- 4-ary constraint
- Predicate constraint

##### Constraint 5: All open non-border cells have to be reachable from the entrance.

To implement this we will simply run a BFS algorithm on every open non-border cell. Once again cells marked as `None` will be treated as open cells.

$$
C_5 =
\begin{cases}
Scope(C_5) = \{X_0, X_1, \ldots, X_{n \times n - 1}\} \\
Relation(C_5) = \operatorname{reachable}(assignment)
\end{cases}
$$

Since we do not define any strict entry point we must consider every possible entry point. We will try every single possible entry point and stop once we find one from which all open non-border cells are reachable.

So `reachable` is defined as follows:

```text
reachable(assignment):
    find possible entry points by considering open (or unassigned) left border variables,
    excluding the corners
    for every entry point:
        for every assigned open non-border cell:
            run BFS
            if BFS is False:
                break and try the next entry point
        return True if all assigned open non-border cells are reachable from this entry point

    return False if no entry point was found from which all open non-border cells are reachable
```

- $n^2$-ary Constraint
- Predicate Constraint

##### Constraint 6: The Labyrinth must be solvable, i.e. a valid path from start to goal must exist

The constraints are not enforced sequentially; therefore, as we did for the reachability constraint, we cannot simply run BFS with a fixed start and goal point. Instead, we must consider every possible start, as well as every possible goal point of the current (partial) assignment and find at least one valid path between one of those. 


$$
C_6 =
\begin{cases}
Scope(C_6) = \{X_0, X_1, \ldots, X_{n \times n - 1}\} \\
Relation(C_6) = \operatorname{solvable}(assignment)
\end{cases}
$$

```text
solvable(assignment):
    for every possible starting point:
        for every possible ending point:
            if BFS is True:
                return True
    return False if no possible solving path was found
```

- $n^2$-ary Constraint
- Predicate Constraint



## Implementation 

### CSP Solver 

Backtracking search 



## Search algorithms to solve a CSP
