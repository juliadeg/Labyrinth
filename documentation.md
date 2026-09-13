


## Labyrinth as a CSP

- Goal: Given a parameter size $n$ and a minimum number of walls $nWalls$ (excluding the border), find a solvable labyrinth constellation with an entry and an exist. 

Problem Formulation as CSP: 

$$
CSP = \langle \mathcal{X}, \mathcal{D}, \mathcal{C} \rangle
$$

#### Variables $\mathcal{X}$

For a $n \times n$ grid we create $n \times n$ variables, each denoting one grid in the labyrinth:

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
\mathcal{X}_{tbborder} = \{X_{B,0}, X_{B,1}, \dots, X_{B,2n}\} \subseteq \mathcal{X}
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

##### Constraint ?: All open cells have to be reachable from the entrance.

##### Constraint ?: Every 2x2 block has to contain at least one open cell. 