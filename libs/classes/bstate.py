from bitarray import frozenbitarray as bitarray
from libs.classes.action import BAction
from libs.classes.state import State

class BState(State):
    def __init__(self,
                 predicates: bitarray=None,
                 cost: int=None,
                 heuristic: int=0,
                 parent_action: str = "",) -> None:
        if cost is None:
            self.cost = float('inf')
        else:
            self.cost = cost
        self.heuristic = heuristic
        self.parent_action = parent_action
        if predicates is None:
            self.predicates = bitarray()
        else:
            self.predicates = predicates

    def conditionHolds(self, precondition: bitarray)->bool:
        return precondition & self.predicates == precondition

    def applyEffects(self, posEffect: bitarray, negEffect: bitarray)->None:
        self.predicates = self.predicates | posEffect
        self.predicates = self.predicates ^ negEffect

    def getSuccessorState(self, action: BAction):
        # TODO: We only consider deterministic actions for the moment,
        #       that is, an action produces only a succesor
        newPredicates = bitarray(self.predicates)
        # Convert positive bits
        newPredicates = self.predicates | action.posEffects
        # Consider negative effects
        newPredicates = newPredicates ^ action.negEffects
        return BState(newPredicates, parent_action=action.name)

    def isApplicable(self, action: BAction)->bool:
        return self.conditionHolds(action.precond)

    def  __str__(self):
        return self.predicates

    def export(self):
        data = {}
        data['predicates'] = list(self.predicates)
        data['cost'] = self.cost
        data['heuristic'] = self.heuristic
        data['parent_action'] = self.parent_action
        return data