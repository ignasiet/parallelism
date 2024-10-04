from bitarray import frozenbitarray as bitarray

class Action():
    def __init__(self,
                 name: str,
                 preconditions: frozenset,
                 posEffects: list,
                 negEffects: list,
                 cost: int=None) -> None:
        self.name=name
        self.precond=frozenset(preconditions)
        self.posEffects=posEffects
        self.negEffects=negEffects
        self.cost=cost

class BAction():
    def __init__(self,
                 name: str,
                 preconditions: bitarray,
                 posEffects: bitarray,
                 negEffects: bitarray,
                 cost: int=None) -> None:
        self.name=name
        self.precond=preconditions
        self.posEffects=posEffects
        self.negEffects=negEffects
        self.cost=cost
