import unittest
from libs.algs.search import Search
from libs.classes import State, Action

class TestSearch(unittest.TestCase):
    def test_isGoal(self):
        s = State(frozenset(['p1','p2','p3']))
        g = frozenset(['p1','p2','p4'])
        se = Search(s, [], g)
        self.assertEqual(se.isGoalState(s,g), False)

    def test_search(self):
        init = State(frozenset(['p1']),
                     cost=0,
                     heuristic=0)
        g = frozenset(['not_p1','p2'])
        action1 = Action('act_1',
                        ['p1'],
                        ['not_p1'],
                        ['p1'],
                        1)
        action2 = Action('act_2',
                        [],
                        ['p2'],
                        [],
                        1)
        se = Search(initialState=init,
                    actions=[action1,action2],
                    goals=g)
        solution = se.start()
        self.assertEqual(solution.conditionHolds(g), True)
        self.assertEqual(solution.cost, 2)

    def test_heuristic(self):
        init = State(frozenset(['p1']),
                     cost=0,
                     heuristic=0)
        g = frozenset(['not_p1','p2'])
        action1 = Action('act_1',
                        ['p1'],
                        ['not_p1'],
                        ['p1'],
                        1)
        action2 = Action('act_2',
                        [],
                        ['p2'],
                        [],
                        1)
        se = Search(init,
                    [action1, action2],
                    g)
        hValue = se.getHeuristicValue(init)
        self.assertEqual(hValue, 2)
    
    def testimposibleHeuristic(self):
        init = State(frozenset(['p1']),
                     cost=0,
                     heuristic=0)
        g = frozenset(['not_p1','p3'])
        action1 = Action('act_1',
                        ['p1'],
                        ['not_p1'],
                        ['p1'],
                        1)
        action2 = Action('act_2',
                        [],
                        ['p2'],
                        [],
                        1)
        se = Search(init,
                    [action1, action2],
                    g)
        hValue = se.getHeuristicValue(init)
        self.assertEqual(hValue, float("inf"))

    def test_correctParents(self):
        init = State(frozenset(['p1']),
                     cost=0,
                     heuristic=0)
        g = frozenset(['not_p1','p2'])
        action1 = Action('act_1',
                        ['p1'],
                        ['not_p1'],
                        ['p1'],
                        1)
        action2 = Action('act_2',
                        [],
                        ['p2'],
                        [],
                        1)
        se = Search(init,
                    [action1, action2],
                    g)


if __name__ == '__main__':
    unittest.main()