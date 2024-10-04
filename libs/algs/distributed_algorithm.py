from libs.classes import State, Action, CostQueue
from typing import List, Generator
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class DAlgorithm():
    def __init__(self,
                 initialState: State,
                 actions: list,
                 goals: frozenset)-> None:
        self.actions = actions
        self.goals = goals
        self.initialState = initialState
        self.initQueue()
        self.openList = {}
        self.closedList = {}
        self.solvedStates = {}
        self.load_functions()

    def load_functions(self):
        pass

    def initQueue(self)->None:
        # Default queue is the cost minimizing queue
        self.queue = CostQueue()

    def resetSearch(self)->None:
        self.initQueue()
        self.openList = {}
        self.closedList = {}

    def expandState(self,
                    state: State,
                    action: Action)->State:
        # TODO: This function must be parallelized in the future
        return state.getSuccessorState(action)
    
    def getHeuristicValue(self,
                          state: State)->int:
        return 0

    def isGoalState(self,
                    state: State,
                    goal: frozenset)->bool:
        return state.conditionHolds(goal)

    def addStatetoClosedList(self,
                             state: State)->None:
        self.closedList[state.predicates]=state

    def addStatetoOpenList(self,
                           state: State)->None:
        self.openList[state.predicates]=state

    def closedListContains(self, state: frozenset)->bool:
        return state.predicates in self.closedList

    def openListContains(self, state: frozenset)->bool:
        return state.predicates in self.openList

    def getStateFromClosedList(self, state: State)->State:
        return self.closedList[state.predicates]

    def getStateFromOpenList(self, state: State)->State:
        return self.openList[state.predicates]

    async def parallel_expansion(self,
                                 current_state: State)->Generator:
        for action in self.actions:
            # Verify if action is applicable, else continue:
            if not current_state.isApplicable(action):
                continue
            logging.debug(f"Applying action: {action.name}")
            next_state = self.expandState(current_state,
                                          action)
            if current_state.cost == float("inf"):
                next_state.cost = action.cost
            else:
                next_state.cost = current_state.cost + action.cost

            if self.openListContains(next_state):
                # Verify if we have the same state with a lesser cost
                if self.getStateFromOpenList(next_state).cost < next_state.cost:
                    logging.debug(f"State already on list with lower cost")
                    continue
            elif self.closedListContains(next_state):
                # Verify if we have to reopen same state
                if self.getStateFromClosedList(next_state).cost < next_state.cost:
                    logging.debug(f"Found state already expanded with lower cost")
                    continue
            else:
                # Obtain heuristic value for nextState
                logging.debug("Computing heuristic")
                next_state.heuristic = await self.getHeuristicValue(next_state)
                logging.debug(f"Heuristic value {next_state.heuristic}")
            yield next_state
