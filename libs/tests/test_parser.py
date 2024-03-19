import unittest
import yaml
from libs.classes import State, Action
from libs.classes.parser import MyParser

class TestParser(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.p = MyParser('libs/problems/problem1.yaml')
        self.p.parse()

    def test_parser(self):
        self.assertEqual(self.p.goal, frozenset(['at_agent_1_pos_4_4']))
        self.assertEqual(self.p.invariants, ['adjacent'])

    def test_parseObjects(self):
        self.assertEqual(len(self.p.objects), 2)
        self.assertEqual(self.p.objects['agent'], ['agent_1'])
        self.assertEqual(len(self.p.objects['pos']), 16)

    def test_combinations(self):
        self.p.parse()
        combination = [{"who": "agent_1"},
                       {"from": "pos_1_1"},
                       {"to": "pos_1_4"}]
        n = self.p.merge_combination(combination)
        self.assertEqual(len(n), 3)
        assert "who" in n

    def test_substituteString(self):
        s_string = self.p.substitute_string(['who','to'],
                                            {'who': 'agent_1','to': 'pos_1'})
        self.assertEqual(s_string, ['agent_1', 'pos_1'])
        effect_replaced = self.p.replace_effect(
            'at',
            {'at': ['who', 'from']},
            {'who': 'agent_1', 'from': 'pos_1'},
        )
        self.assertEqual(effect_replaced, 'at_agent_1_pos_1')
        new_comb = self.p.merge_combination([{'who': 'agent_1'},
                                             {'from': 'pos_1_1'},
                                             {'to': 'pos_1_4'}])
        self.assertEqual(new_comb, {'who': 'agent_1', 'from': 'pos_1_1', 'to': 'pos_1_4'})

    def test_parseInit(self):
        self.assertEqual(self.p.getInitState().cost, float("inf"))
        self.assertEqual(self.p.getInitState().heuristic, 0)

    def test_validity(self):
        with open('libs/problems/problem1.yaml', 'r') as file:
            problem = yaml.safe_load(file)['problem']
        combination = {"who": "agent_1",
                       "from": "pos_1_1",
                       "to": "pos_1_4"}
        self.p.check_validity(combination, problem['actions'][0])
        self.assertEqual(self.p.check_validity(combination, problem['actions'][0]), False)

    def test_parsePreconditions(self):
        action_string = {'name': 'move',
                         'parameters': [{'who': 'agent'}, {'from': 'pos'}, {'to': 'pos'}],
                         'precond': {'at': ['who', 'from'],
                                     'adjacent': ['from', 'to']},
                         'effect': {'pos': [{'at': ['who', 'to']}],
                                    'neg': [{'at': ['agent', 'to']}]}
                        }
        combination = self.p.merge_combination([{'who': 'agent_1'},
                                                {'from': 'pos_1_1'},
                                                {'to': 'pos_1_2'}])
        preconditions = self.p.parse_preconditions(action_string['precond'],
                                                   combination)
        assert 'at_agent_1_pos_1_1' in preconditions
        assert 'adjacent_pos_1_1_pos_1_2' not in preconditions
        self.assertEqual(len(preconditions), 1)

    def test_parseEffects(self):
        action_string = {'name': 'move',
                         'parameters': [{'who': 'agent'}, {'from': 'pos'}, {'to': 'pos'}],
                         'precond': {'at': ['who', 'from'],
                                     'adjacent': ['from', 'to']},
                         'effect': {'pos': [{'at': ['who', 'to']}],
                                    'neg': [{'at': ['who', 'from']}]}
                        }
        combination = self.p.merge_combination([{'who': 'agent_1'},
                                                {'from': 'pos_1_1'},
                                                {'to': 'pos_1_2'}])
        p_effects = self.p.parse_effects(action_string['effect']['pos'],
                                         combination)
        assert 'at_agent_1_pos_1_1' not in p_effects
        assert 'at_agent_1_pos_1_2' in p_effects
        self.assertEqual(len(p_effects), 1)

    def test_parseActions(self):
        self.assertEqual(len(self.p.actions), 33)


if __name__ == '__main__':
    unittest.main()