from libs.classes import State, BState, Action, CostQueue, BAction

class Algorithm():
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
        self.loadFunctions()

    def loadFunctions(self):
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
