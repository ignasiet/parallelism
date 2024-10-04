import unittest
from libs.classes.bstate import BState
from libs.classes.action import BAction
from bitarray import frozenbitarray as bitarray

class TestBState(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.state=BState(bitarray('0010101000'))
        # state = 0010101000

    def test_state(self):
        self.assertEqual(self.state.cost, float('inf'))
        self.assertEqual(len(self.state.predicates), 10)

    def test_conditionHolds(self):
        condition1=bitarray('0010100000')
        self.assertEqual(self.state.conditionHolds(condition1), True)

    def test_applyEffects(self):
        negEffect=bitarray('0010000000')
        posEffect=bitarray('1000000001')
        self.state.applyEffects(posEffect=posEffect,
                                negEffect=negEffect)
        self.assertEqual(self.state.predicates, bitarray('1000101001'))

    def test_isApplicable(self):
        self.state = BState(bitarray('1000101001'))
        action = BAction('example',
                         bitarray('1000000000'),
                         bitarray('1100000000'),
                         bitarray('0000000001'),
                         0)
        self.assertEqual(self.state.isApplicable(action), True)

    def test_isEmptyActionApplicable(self):
        self.state = BState(bitarray('1000101001'))
        action = BAction('example',
                        bitarray('0000000000'),
                        bitarray('0000000010'),
                        bitarray('0000000001'),
                        0)
        self.assertEqual(self.state.isApplicable(action), True)
    
    def test_getSuccessorState(self):
        self.state=BState(bitarray('1000101001'))
        action = BAction('example',
                         bitarray('1000000001'),
                         bitarray('1100000000'),
                         bitarray('0000000001'),
                         0)

        nxtState = self.state.getSuccessorState(action)
        self.assertEqual(nxtState.predicates, bitarray('1100101000'))
        self.assertNotEqual(nxtState.predicates, self.state.predicates)


if __name__ == '__main__':
    unittest.main()
