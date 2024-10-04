import yaml
from libs.classes import Action, State, BState
from libs.classes.mapper import Mapper
import itertools

POS_KEYWORD = 'pos'
NEG_KEYWORD = 'neg'

class MyParser():
    def __init__(self,
                 path: str):
        self.file_path = path
        self.instantiations = set()
        with open(self.file_path, 'r') as file:
            problem = yaml.safe_load(file)['problem']
            self.name = problem['name']
            self.objects = self.parse_objects(objects=problem['objects'])
            self.predicates = problem['predicates']
            self.invariants = self.calculate_invariants(actions=problem['actions'],
                                                        predicates=list(self.predicates.keys()))
            self.init = frozenset(problem['init'])
            self.goal = frozenset(problem['goal'])
            self.actions = self.parse_actions(problem['actions'])
        self.clean_state()
        self.mapper = Mapper(self.instantiations)

    def getInitState(self,
                     binarization: bool)->State:
        if binarization:
            return BState(predicates=self.mapper.translatePredicates(self.init))
        return State(predicates=self.init)
    
    def getActions(self,
                   binarization: bool)->list:
        if binarization:
            return [self.mapper.convertAction(action) for action in self.actions if self.mapper.convertAction(action) is not None]
        return self.actions
    
    def getGoal(self,
                binarization: bool)->State:
        if binarization:
            return self.mapper.translatePredicates(self.goal)
        return self.goal

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
            print(ef)
            # positive effects variants
            if self.has_effect(POS_KEYWORD,ef):
                for pe in ef['pos']:
                    variants.extend([p for p in pe if p not in variants])
            # negative effects variants
            if self.has_effect(NEG_KEYWORD,ef):
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
            that is, if it is not an (invariant and not present at initial state)
            OTHER TYPE OF INVARIANTS: impossible preconditions
        """
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
        if self.has_effect(POS_KEYWORD, effects):
            instantiated_pos_effects = self.parse_effects(
                effects['pos'],
                combination)
            # Add all instantiated predicates to the instatiations list
            self.instantiations.update(instantiated_pos_effects)
        else:
            instantiated_pos_effects = []

        # negative
        if self.has_effect(NEG_KEYWORD, effects):
            instantiated_neg_effects = self.parse_effects(
                effects['neg'],
                combination)
            self.instantiations.update(instantiated_neg_effects)
        else:
            instantiated_neg_effects = []


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
        if self.invariants:
            temp_init = []
            for item in self.init:
                if item.split('_')[0] not in self.invariants:
                    print(f"Adding predicate: {item}")
                    temp_init.append(item)
                # for inv in self.invariants:
                #     if not item.startswith(inv):
                #         print(f"Adding predicate: {item}")
                #         temp_init.append(item)
            self.init = frozenset(temp_init)

    def has_effect(self,
                   keyword,
                   effects):
        return keyword in effects
