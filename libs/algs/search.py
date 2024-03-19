from libs.classes import State
from libs.algs.algorithm import Algorithm
from libs.algs.heuristic import Heuristic

# Implementation based on:
# https://mat.uab.cat/~alseda/MasterOpt/AStar-Algorithm.pdf
class Search(Algorithm):

    def loadFunctions(self)->None:
        self.heuristicSearch = Heuristic(initialState=self.initialState,
                                         actions=self.actions,
                                         goals=self.goals
                                        )

    def getHeuristicValue(self, state: State) -> int:
        return self.heuristicSearch.getHValue(state)

    def start(self)->State:
        self.queue.addElement(self.initialState)
        while not self.queue.isEmpty():
            # This algorithm works as follows:
            # 1 First get lowest cost state from queue
            currentStateFCost, _, current_state = self.queue.getNextState()
            # 2 if it is a goal state, break
            if self.isGoalState(current_state, self.goals):
                break
            # 3 Generate its succesors
            # Each successor has cost = parent_cost + action_cost
            for action in self.actions:
                # Verify if action is applicable, else continue:
                if not current_state.isApplicable(action):
                    continue
                next_state = self.expandState(current_state,
                                             action)
                if current_state.cost == float("inf"):
                    next_state.cost = action.cost
                else:
                    next_state.cost = current_state.cost + action.cost
                if self.openListContains(next_state):
                    # Verify if we have the same state with a lesser cost
                    if self.getStateFromOpenList(next_state).cost < next_state.cost:
                        continue
                elif self.closedListContains(next_state):
                    # Verify if we have to reopen same state
                    if self.getStateFromClosedList(next_state).cost < next_state.cost:
                        continue
                else:
                    # Obtain heuristic value for nextState
                    # for testing we will use 0 heuristic
                    next_state.heuristic = self.getHeuristicValue(next_state)
                # In this step the nextState is either:
                # a) an state with a lesser cost than the same state found previously
                # b) an state with a lesser cost than the same state closed previously
                # c) a new state
                # Everytime we add to the open list
                # we must also add to the current queue
                # print(f"Adding next state: {nextState} with cost {nextState.cost} and h {nextState.heuristic}")
                self.queue.addElement(next_state)
                self.addStatetoOpenList(next_state)
                # We want to keep track of each state parent:
                self.solvedStates[next_state.predicates] = current_state
            # We send the current state to the closed list, because we expanded it:
            self.addStatetoClosedList(current_state)
        if not self.isGoalState(current_state, self.goals):
            print('Error: solution not found.')
            return current_state

        print(f'Solution found: {current_state.predicates}')
        self.getStats(current_state)
        return current_state

    def getStats(self, goal_state: State):
        expandedStates = len(self.solvedStates)
        solution = []
        states_path = []
        pState = goal_state.predicates
        solution.append(goal_state.parent_action)
        while pState != self.initialState.predicates:
            solution.append(self.solvedStates[pState].parent_action)
            pState = self.solvedStates[pState].predicates
        solution_size = len(solution)
        print("**********************")
        print(f"Expanded states: {expandedStates}")
        print(f"Solution: {solution}")
        print(f"Solution size: {solution_size}")
