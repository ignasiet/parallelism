from libs.classes.action import Action

class State():
    def __init__(self,
                 predicates: frozenset=None,
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
            self.predicates = frozenset()
        else:
            self.predicates = predicates

    def addPredicate(self, literal: str)->None:
        self.predicates.add(literal)

    def removeLiteral(self, literal: str)->None:
        if literal in self.predicates:
            self.predicates.remove(literal)
    
    def conditionHolds(self, precondition: frozenset)->bool:
        return precondition.issubset(self.predicates)

    def applyEffects(self, posEffect: frozenset, negEffect: frozenset)->None:
        self.predicates = self.predicates.difference(negEffect)
        self.predicates = self.predicates.union(posEffect)
    
    def getSuccessorState(self, action: Action):
        # TODO: We only consider deterministic actions for the moment,
        #       that is, an action produces only a succesor
        newPredicates = self.predicates.copy()
        newPredicates = newPredicates.difference(action.negEffects)
        newPredicates = newPredicates.union(action.posEffects)
        return State(newPredicates, parent_action=action.name)

    def isApplicable(self, action: Action)->bool:
        return self.conditionHolds(action.precond)
