import unittest
from libs.classes.state import State
from libs.classes.action import Action

class TestState(unittest.TestCase):
    def test_state(self):
        state=State(set(['p1','p1','p1']))
        self.assertEqual(state.cost, float('inf'))
        self.assertEqual(len(state.predicates), 1)

    def test_conditionHolds(self):
        state=State(set(['p1','p2','p3']))
        condition1=set(['p2','p1'])
        self.assertEqual(state.conditionHolds(condition1), True)

    def test_applyEffects(self):
        state=State(set(['p1','p2','p3']))
        negEffect=set(['p3'])
        posEffect=set(['e1'])

        state.applyEffects(posEffect=posEffect,
                           negEffect=negEffect)
        self.assertEqual(state.predicates, set(['p1','p2','e1']))
    
    def test_isApplicable(self):
        action = Action('example',
                        ['p1','p2'],
                        ['e1','e2'],
                        ['p1','p2'],
                        0)
        state=State(set(['p1','p2','p3']))
        self.assertEqual(state.isApplicable(action), True)
    
    def test_isEmptyActionApplicable(self):
        action = Action('example',
                        [],
                        ['e1','e2'],
                        ['p1','p2'],
                        0)
        state=State(set(['p1','p2','p3']))
        self.assertEqual(state.isApplicable(action), True)
    
    def test_getSuccessorState(self):
        state=State(set(['p1','p2','p3']))
        action = Action('example',
                        ['p1','p2'],
                        ['e1','e2'],
                        ['p1','p2'],
                        0)

        nxtState = state.getSuccessorState(action)
        self.assertEqual(nxtState.predicates, set(['e1','e2','p3']))
        self.assertNotEqual(nxtState, state)


if __name__ == '__main__':
    unittest.main()