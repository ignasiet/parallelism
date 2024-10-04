from bitarray import frozenbitarray, bitarray
from libs.classes import Action, BAction

class Mapper():
    def __init__(self,
                 instantiations: set) -> None:
        self.basiclenght = len(instantiations)
        self.mapper = {}
        i = 0
        for elem in instantiations:
            self.mapper[elem] = i
            i+=1

    def translatePredicates(self,
                            predicates: frozenset)->frozenbitarray:
        """ This is the function used to translate states to bit arrays
            POSSIBLE BUG: Invariant are not to be translated. Some predicates, result of impossible
            actions may end here and not have a mmaping defined on the mapper.
        """
        state = bitarray(self.basiclenght)
        for pred in predicates:
            if pred not in self.mapper:
                raise Exception("Predicate not in the mapper list")
            state[self.mapper[pred]] = True
        return frozenbitarray(state)

    def convertAction(self,
                      action: Action)->BAction:
        """ This is the function used to translate actions to bit arrays.
            Type hints for actions should not be considered
        """
        try:
            a = BAction(action.name,
                        self.translatePredicates(action.precond),
                        self.translatePredicates(action.posEffects),
                        self.translatePredicates(action.negEffects),
                        action.cost)
            return a
        except Exception as e:
            print(f"Dropping action: {action.name}")
            return None
