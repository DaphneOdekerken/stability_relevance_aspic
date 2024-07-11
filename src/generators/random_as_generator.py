import random
from typing import Dict

from src.classes.argumentation_system import ArgumentationSystem
from src.classes.defeasible_rule import DefeasibleRule
from src.classes.literal import Literal


class RandomArgumentationSystemGenerator:
    def __init__(self, nr_of_literals: int,
                 rule_antecedent_distribution: Dict[int, int],
                 allow_inconsistent_antecedents: bool = True):
        if nr_of_literals % 2 != 0:
            raise ValueError('Language size should be even, since each '
                             'literal should have a negated version.')
        self.language_size = nr_of_literals
        self.rule_size = sum(rule_antecedent_distribution.values())
        self.rule_antecedent_distribution = rule_antecedent_distribution
        if any([nr_antecedents > nr_of_literals / 2
                for nr_antecedents in
                self.rule_antecedent_distribution.keys()]):
            raise ValueError('Rules cannot have more antecedents than half of '
                             'the language size.')
        self.allow_inconsistent_antecedents = allow_inconsistent_antecedents

    def generate(self) -> ArgumentationSystem:
        # Generate language with contradictories (strong negation).
        positive_language_size = int(self.language_size / 2)
        language = {}
        contradictories = {}
        for pos_literal_index in range(positive_language_size):
            literal_str_positive = 'l' + str(pos_literal_index)
            literal_str_negative = 'not_l' + str(pos_literal_index)

            literal_pos = Literal(literal_str_positive)
            literal_neg = Literal(literal_str_negative)

            language[literal_str_positive] = literal_pos
            language[literal_str_negative] = literal_neg

            contradictories[literal_str_positive] = {literal_neg}
            contradictories[literal_str_negative] = {literal_pos}

        rules = []
        rule_index = 0

        for number_of_antecedents, number_of_rules in \
                self.rule_antecedent_distribution.items():
            for rule_index_within_antecedent_round in range(number_of_rules):
                # Consequent
                rule_consequent = random.choice(list(language.values()))

                # Antecedents
                rule_antecedents = set()
                antecedent_candidates = [literal for literal in
                                         language.values()]
                for antecedent_index in range(number_of_antecedents):
                    if len(antecedent_candidates) == 0:
                        break
                    new_antecedent = random.choice(antecedent_candidates)
                    rule_antecedents.add(new_antecedent)
                    antecedent_candidates.remove(new_antecedent)
                    if not self.allow_inconsistent_antecedents:
                        if new_antecedent.negation in antecedent_candidates:
                            antecedent_candidates.remove(
                                new_antecedent.negation)

                # Description / name
                new_rule = DefeasibleRule(str(rule_index), rule_antecedents,
                                          rule_consequent)
                rules.append(new_rule)
                rule_index += 1

        argumentation_system = ArgumentationSystem(
            language, contradictories, [], rules, None, False)
        return argumentation_system
