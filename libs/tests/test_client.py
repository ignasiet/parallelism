# ['free_room_1_thursday', 'free_room_1_friday', 'free_room_1_monday', 'free_room_1_wednesday', 'free_room_1_tuesday']
# ['free_room_1_friday', 'free_room_1_tuesday', 'free_room_1_thursday', 'free_room_1_wednesday', 'scheduled_agent_1_agent_2_room_1_monday']

# Test special strange states on heuristic fuction:
import unittest
from libs.classes.parser import MyParser
from libs.distributed.client import AstarClient
from libs.classes import State

class TestClient(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        path = "libs/problems/schedule3.yaml"
        p = MyParser(path)
        binary_rep = False
        self.client = AstarClient(initialState=p.getInitState(binary_rep),
                                actions=p.getActions(binary_rep),
                                goals=p.getGoal(binary_rep))

    def test_getNextStateHeuristicValue1(self):
        state1=State(frozenset(['free_room_1_thursday',
                                 'free_room_1_friday',
                                 'free_room_1_monday',
                                 'free_room_1_wednesday',
                                 'free_room_1_tuesday',
                                ]
                            ),
                     cost=0,
                     heuristic=0
                    )

        h_value = self.client.getHeuristicValue(state1)
        self.assertEqual(h_value, 4)

    def test_getNextStateHeuristicValue2(self):
        state1=State(frozenset(['free_room_1_friday',
                                'free_room_1_tuesday',
                                'free_room_1_thursday',
                                'free_room_1_wednesday',
                                'scheduled_agent_1_agent_2_room_1_monday']
                            ),
                     cost=0,
                     heuristic=0
                    )

        h_value = self.client.getHeuristicValue(state1)
        self.assertEqual(h_value, 3)

    def test_getNextStateHeuristicValue3(self):
        state1=State(frozenset(['free_room_1_friday',
                                'scheduled_agent_1_agent_3_room_1_tuesday',
                                'free_room_1_thursday',
                                'free_room_1_wednesday',
                                'scheduled_agent_1_agent_2_room_1_monday']
                            ),
                     cost=0,
                     heuristic=0
                    )

        h_value = self.client.getHeuristicValue(state1)
        self.assertEqual(h_value, 2)

if __name__ == '__main__':
    unittest.main()
