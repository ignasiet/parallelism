from libs.algs.algorithm import Algorithm
from libs.classes import State, Action

class Heuristic(Algorithm):

    # def getSuccessorState(self, action: Action):
    #     newPredicates = self.predicates.copy()
    #     newPredicates = newPredicates.difference(action.negEffects)
    #     newPredicates = newPredicates.union(action.posEffects)
    #     return State(newPredicates)

    def getHValue(self,
                  initialState: State)->int:
        # A star heuristic is like regular search without using the negative effects lists
        # TODO: Verify why on heuristics parents cost are inherited
        self.resetSearch()
        self.queue.addElement(initialState.copyEmpty())
        # if self.isGoalState(initialState, self.goals):
        #     return 0
        while not self.queue.isEmpty():
            # This algorithm works as follows:
            # 1 First get lowest cost state from queue
            _, _, currentState = self.queue.getNextState()
            # 2 if it is a goal state, break
            if self.isGoalState(currentState, self.goals):
                if currentState.cost == float("inf"):
                    currentState.cost = 0
                break
            # 3 Generate its succesors
            for action in self.actions:
                # Verify if action is applicable, else continue:
                if not currentState.isApplicable(action):
                    continue
                nextState = self.expandState(currentState,
                                             action)
                if currentState.cost == float("inf"):
                    nextState.cost = action.cost
                else:
                    nextState.cost = currentState.cost + action.cost
                if self.openListContains(nextState) or self.closedListContains(nextState):
                    continue
                self.queue.addElement(nextState)
                self.addStatetoOpenList(nextState)
            # We send the current state to the closed list, because we expanded it:
            self.addStatetoClosedList(currentState)
        if not self.isGoalState(currentState, self.goals):
            print(f'Dead state found: {currentState.export()}')
            return float("inf")
        return currentState.cost
