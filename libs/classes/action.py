class Action():
    def __init__(self,
                 name: str,
                 preconditions: list,
                 posEffects: list,
                 negEffects: list,
                 cost: int=None) -> None:
        self.name=name
        self.precond=frozenset(preconditions)
        self.posEffects=posEffects
        self.negEffects=negEffects
        self.cost=cost
