import yaml
from libs.classes import Action, State
import itertools

class MyParser():
    def __init__(self,
             file: str):
        self.file_path = file
        self.actions = []
        self.name = ''
        self.objects = []
        self.init = []
        self.predicates = {}
        self.invariants = []
        self.goal = ''

    def getInitState(self)->State:
        return State(predicates=self.init)

    def parse(self):
        with open(self.file_path, 'r') as file:
            problem = yaml.safe_load(file)['problem']
            self.name = problem['name']
            self.init = frozenset(problem['init'])
            self.objects = self.parse_objects(objects=problem['objects'])
            self.goal = frozenset(problem['goal'])
            self.predicates = problem['predicates']
            self.invariants = self.calculate_invariants(actions=problem['actions'],
                                                        predicates=list(self.predicates.keys()))
            self.actions = self.parse_actions(problem['actions'])
            self.clean_state()

    def parse_objects(self,
                      objects: list):
        objects_dict = {}
        for obj in objects:
            objects_dict.update(obj)
        return objects_dict

    def calculate_invariants(self,
                             actions: list,
                             predicates: list)->list:
        """ Invariants are predicates that do not appear in any effect, that is they do not
            change value (pos or negative)
        """
        variants = []
        for action in actions:
            ef = action['effect']
            # positive effects variants
            for pe in ef['pos']:
                variants.extend([p for p in pe if p not in variants])
            # negative effects variants
            for ne in ef['neg']:
                variants.extend([p for p in ne if p not in variants])
        return list(set(predicates)-set(variants))

    def parse_actions(self, actions: list)->list[Action]:
        grounded_actions = []
        for a in actions:
            params = a['parameters']
            mapping = []
            for param in params:
                # there is only one key, value for each param
                for arg,obj in param.items():
                    elems = []
                    for elem in self.objects[obj]:
                        elems.append({arg: elem})
                    mapping.append(elems)
            for combination in itertools.product(*mapping):
                comb = self.merge_combination(combination)
                if self.check_validity(comb, a):
                    grounded_actions.append(self.instantiate_action(comb, a))
        return grounded_actions

    def check_validity(self,
                       combination: list,
                       action: dict)->bool:
        """This function will check the validity of the arguments,
            to verify if a combination of parameters is correct,
            that is, if it is not an invariant and not present at initial state"""
        preconditions = action['precond']
        for predicate in preconditions.keys():
            if predicate in self.invariants:
                replaced_e = self.replace_effect(predicate,
                                                 preconditions,
                                                 combination)
                if replaced_e in self.init:
                    return True
                return False
        return True

    def merge_combination(self,
                          combination: list)->dict:
        """This function will transform a list of dicts into a merged dict
        """
        new_combination = combination[0]
        for elem in combination:
            new_combination.update(elem)
        return new_combination

    def substitute_string(self,
                          predicates: list,
                          substitution: dict)->list:
        return [elem.replace(elem, substitution[elem]) for elem in predicates]

    def replace_effect(self,
                       predicate: str,
                       predicates: dict,
                       combination: dict
                       ):
        substitute = self.substitute_string(
                    predicates[predicate],
                    combination,
                )
        return predicate + '_' + '_'.join(substitute)

    def instantiate_action(self, combination, action)->Action:
        preconditions = action['precond']
        instantiated_precond = self.parse_preconditions(
            preconditions,
            combination)

        # Instantiate effects
        # positive
        effects = action['effect']
        instantiated_pos_effects = self.parse_effects(
            effects['pos'],
            combination)

        # negative
        instantiated_neg_effects = self.parse_effects(
            effects['neg'],
            combination)

        name_elements = [f"{k}_{v}" for k,v in combination.items()]
        action_name = action['name']+ "_" + "_".join(name_elements)
        a = Action(name=action_name,
                   preconditions=instantiated_precond,
                   posEffects=instantiated_pos_effects,
                   negEffects=instantiated_neg_effects,
                   cost=1,
                   )
        return a

    def parse_preconditions(self,
                            preconditions: dict,
                            combination: list)->list:
        # Instantiate preconditions
        instantiated_precond = []
        for precondition in preconditions.keys():
            # Invariants are not to be added
            if precondition in self.invariants:
                continue
            instantiated = self.substitute_string(
                preconditions[precondition],
                combination,
            )
            predicate = precondition + '_' + '_'.join(instantiated)
            instantiated_precond.append(predicate)
        return instantiated_precond

    def parse_effects(self,
                      effects: dict,
                      combination: list)->list:
        merged_effects = self.merge_combination(effects)
        instantiates_effects = []
        for p_effect in merged_effects.keys():
            instantiates_effects.append(self.replace_effect(
                p_effect,
                merged_effects,
                combination))
        return instantiates_effects

    def clean_state(self):
        temp_init = []
        for inv in self.invariants:
            for item in self.init:
                if not item.startswith(inv):
                    print(f"Adding predicate: {item}")
                    temp_init.append(item)
        self.init = frozenset(temp_init)
