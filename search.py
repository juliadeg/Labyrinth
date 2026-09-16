from collections import deque
from labyrinth import Position, grid
import time
import visualise as show

actions = [
    (-1, 0), 
    (1, 0), 
    (0,-1), 
    (0,1)
]

class Labyrinth:
    def __init__(self, grid: list[list[int]] | list[int]): 
        if isinstance(grid[0], int): 
            None
            # TO-DO: Turn Flat list into matrix
        else: 
            self.grid = grid

    def is_wall(self, pos: Position) -> bool: 
        return self.grid[pos.x][pos.y] == 1

    def is_inside(self, pos: Position) -> bool:
        return (0 <= pos.x < len(self.grid) and 0 <= pos.y < len(self.grid[pos.x]))


class State:
    lab: Labyrinth = None

    def __init__(self, agent_position: Position, lab: Labyrinth):
        self.agent_position = agent_position 
        # self.lab = lab

        # Only inisitalise labyrinth once
        if State.lab == None:
            State.lab = lab

    # define comparison of two states
    def __eq__(self, other):
        # sanity check whether other is a State object 
        if not isinstance(other, State):
            return NotImplemented
        return (self.agent_position == other.agent_position)

    #def is_goal(self, goal: Position) -> bool:
    #    return self.agent_position == goal

    
def transition(current_state: State, action: tuple) -> State:

    newPos = Position(current_state.agent_position.x + action[0], current_state.agent_position.y + action[1])

    if current_state.lab.isInside(newPos):
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
    def BFS(self, start: Position, goal: Position, labyrinth: Labyrinth): 
        queue = deque()

        start_state = State(start, labyrinth)
        goal_state = State(goal, labyrinth)

        queue.append(start_state)

        # Store only coordinate tuples for the path reconstruction
        previous = {start_state.agent_position.toTuple(): None}

        previous_position = None

        while queue: 
            state = queue.popleft()
            if state.isGoal():
                return True

            for action in actions: 

                newState = transition(state, action)

                if newState: 

                    newStateCoord = newState.agent_position.toTuple()

                    if newStateCoord not in previous:
                        previous[newStateCoord] = state.agent_position.toTuple()
                        queue.append(newState)
        return False

    def DFS(self): 
        stack = []

        stack.append(self.start_state)

        previous = {self.start_state.agent_position.toTuple(): None}
    
        previous_position = None

        while stack: 
            state = stack.pop()
            if state.is_goal(goal): 
                return True

            state_coordinates = state.agent_position.toTuple()

            for action in actions:
                new_state = transition(state, action)

                if new_state:
                    new_state_coordinates = new_state.agent_position.toTuple()

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
                        new_state_coordinates = new_state.agent_position.toTuple()
    
                        if new_state_coordinates not in current_path:
                            stack.append(new_state)
        return result




