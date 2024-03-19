import unittest
from libs.classes.queue import CostQueue
from libs.classes.state import State

class TestQueue(unittest.TestCase):
    def test_getNextState(self):
        state1=State(frozenset(['p1']), 3)
        state2=State(frozenset(['p2']), 2)
        state3=State(frozenset(['p3']), 1)

        q = CostQueue()
        self.assertEqual(q.isEmpty(), True)
        
        q.addElement(state1)
        q.addElement(state2)
        q.addElement(state3)
        self.assertEqual(q.getNextState()[2], state3)
        self.assertEqual(q.getNextState()[2], state2)
        self.assertEqual(q.getNextState()[2], state1)

if __name__ == '__main__':
    unittest.main()