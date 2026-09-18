from collections import deque
# from labyrinth import grid
import time
import visualise as show

actions = [
    (-1, 0), 
    (1, 0), 
    (0,-1), 
    (0,1)
]

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


class Labyrinth:
    def __init__(self, grid: list[list[int]] | list[int], n: int | None = None): 

        # Assign n 
        if n is None and isinstance(grid[0], list):
            n_rows = len(grid)
            n_cols = len(grid[0]) #TO-DO: Check that all rows are the same size

            if n_cols == n_rows: 
                self.n = n_cols

            #TO-DO: else: return error 
        else: 
            self.n = n 

        # Assign grid 
        if isinstance(grid[0], int): 
            matrix = []
            for i in range(0, len(grid), n): 
                matrix.append(grid[i:i+n])
            self.grid = matrix
        else: 
            self.grid = grid

    def is_wall(self, pos: Position) -> bool: 
        return self.grid[pos.x][pos.y] == 1

    def is_inside(self, pos: Position) -> bool:
        return (0 <= pos.x < len(self.grid) and 0 <= pos.y < len(self.grid[pos.x]))


class State:
    # lab: Labyrinth = None

    def __init__(self, agent_position: Position, lab: Labyrinth):
        self.agent_position = agent_position 
        self.lab = lab

        # Only inisitalise labyrinth once
        # if State.lab == None:
        #    State.lab = lab

    # define comparison of two states
    def __eq__(self, other):
        # sanity check whether other is a State object 
        if not isinstance(other, State):
            return NotImplemented
        return (self.agent_position == other.agent_position)

    # TO DO: remove is_goal and use operator overloading instead
    # def is_goal(self, goal: Position) -> bool:
    #    return self.agent_position == goal

    
def transition(current_state: State, action: tuple) -> State:

    newPos = Position(current_state.agent_position.x + action[0], current_state.agent_position.y + action[1])

    if current_state.lab.is_inside(newPos):
        if current_state.lab.is_wall(newPos): 
            return None
        else: 
            return State(newPos, current_state.lab)
    else: 
        return None

## Search Algorithms

class Search: 
    def __init__(self, start: Position, goal: Position, labyrinth: Labyrinth):
        self.start_state = State(start, labyrinth)
        self.goal_state = State(goal, labyrinth)
        self.labyrinth = labyrinth 

    @staticmethod
    def BFS(start: Position, goal: Position, labyrinth: Labyrinth) -> bool: 
        queue = deque()

        start_state = State(start, labyrinth)
        goal_state = State(goal, labyrinth)

        queue.append(start_state)

        # Store only coordinate tuples for the path reconstruction
        previous = {start_state.agent_position.to_tuple(): None}

        previous_position = None

        while queue: 
            state = queue.popleft()
            if state == goal_state:
                return True

            for action in actions: 

                newState = transition(state, action)

                if newState: 

                    newStateCoord = newState.agent_position.to_tuple()

                    if newStateCoord not in previous:
                        previous[newStateCoord] = state.agent_position.to_tuple()
                        queue.append(newState)
        return False

    def DFS(self): 
        stack = []

        stack.append(self.start_state)

        previous = {self.start_state.agent_position.to_tuple(): None}
    
        previous_position = None

        while stack: 
            state = stack.pop()
            if state == self.goal_state: 
                return True

            state_coordinates = state.agent_position.to_tuple()

            for action in actions:
                new_state = transition(state, action)

                if new_state:
                    new_state_coordinates = new_state.agent_position.to_tuple()

                    if new_state_coordinates not in previous:
                        previous[new_state_coordinates] = state_coordinates
                        stack.append(new_state)

        return False


    def is_cycle(self, state: State): 
        pass

    def DLS(self, limit: int): 

        depth = 0 

        current_path = []

        stack = [] 

        stack.append(self.start_state)

        result = False

        while stack: 
            state = stack.pop()
            if state is self.goal_state: 
                return state
            # Cut off
            if depth > limit: 
                return False
            elif not self.is_cycle(state):

                # Append all children 
                for action in actions:
                    new_state = transition(state, action)

                    if new_state:
                        new_state_coordinates = new_state.agent_position.to_tuple()
    
                        if new_state_coordinates not in current_path:
                            stack.append(new_state)
        return result



