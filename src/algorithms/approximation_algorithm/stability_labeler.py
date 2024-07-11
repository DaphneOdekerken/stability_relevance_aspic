from typing import Dict, Set

from .satisfiability_labeler import SatisfiabilityLabeler
from .stability_labels import StabilityLabels
from ..stability_result import StabilityResult
from ...classes.defeasible_rule import DefeasibleRule
from ...classes.incomplete_argumentation_theory import \
    IncompleteArgumentationTheory
from ...classes.literal import Literal
from ...import_export.iat_from_lp_reader import read_from_lp_file


class StabilityLabeler:
    def __init__(self):
        pass

    def solve_stability(self, iat_path) -> \
            StabilityResult:
        iat = read_from_lp_file(iat_path)

        # Preprocessing: take the initial labeling from the
        # SatisfiabilityLabeler
        labels = SatisfiabilityLabeler().solve_stability(iat)
        rules_visited = {rule: False
                         for rule in iat.argumentation_system.defeasible_rules}

        # Connect literals, so we can ask for their children and parents
        all_literals = iat.argumentation_system.language.values()
        parents = {literal: set() for literal in all_literals}
        children = {literal: set() for literal in all_literals}
        for rule in iat.argumentation_system.defeasible_rules:
            for antecedent in rule.antecedents:
                parents[antecedent].add(rule)
            children[rule.consequent].add(rule)

        # Start by coloring leaves (literals for which there is no rule) and
        # observables
        leaves_and_observables = [
            literal for literal in all_literals
            if not children[literal] or iat.is_queryable(literal)]
        rules_to_reconsider = set()
        for literal in leaves_and_observables:
            self._color_literal(iat, literal, labels, children)
            rules_to_reconsider = rules_to_reconsider | parents[literal]

        # Color rules and (contraries of) their conclusions
        while rules_to_reconsider:
            rule = rules_to_reconsider.pop()

            # Store old label, so we can check if the label changed.
            old_rule_label = labels.rule_labeling[rule].__copy__()

            self._color_rule(rule, labels)

            # If this was the first time the rule was considered or if its
            # label changed, it may influence others.
            if not rules_visited[rule] or \
                    labels.rule_labeling[rule] != old_rule_label:
                old_literal_label = \
                    labels.literal_labeling[rule.consequent].__copy__()
                self._color_literal(iat, rule.consequent, labels, children)
                if labels.literal_labeling[rule.consequent] != \
                        old_literal_label:
                    rules_to_reconsider = rules_to_reconsider | \
                                          parents[rule.consequent]
                for contrary_literal in \
                        rule.consequent.contraries_and_contradictories:
                    old_contrary_literal_label = \
                        labels.literal_labeling[contrary_literal].__copy__()
                    self._color_literal(iat, contrary_literal, labels,
                                        children)
                    if labels.literal_labeling[contrary_literal] != \
                            old_contrary_literal_label:
                        rules_to_reconsider = rules_to_reconsider | \
                                              parents[contrary_literal]
                rules_visited[rule] = True

        stability_result = labels.to_stability_result()
        return stability_result

    @staticmethod
    def _color_literal(iat: IncompleteArgumentationTheory, literal: Literal,
                       labels: StabilityLabels,
                       children: Dict[Literal, Set[DefeasibleRule]]):
        """
        Color the Literal, that is: check, based on observations/rules for
        this literal/rules for its contraries, if
        this Literal can still become unsatisfiable/defended/out/blocked.
        """
        if iat.is_queryable(literal) and literal in iat.knowledge_base:
            # L-U-a: The literal is observed, so it cannot be unsatisfiable.
            labels.literal_labeling[literal].unsatisfiable = False
        elif any([not labels.rule_labeling[rule].unsatisfiable
                  for rule in children[literal]]):
            # L-U-b: There is a rule-based argument for the literal,
            # so it cannot be unsatisfiable.
            labels.literal_labeling[literal].unsatisfiable = False

        if iat.is_queryable(literal):
            if any([contrary_literal in iat.knowledge_base
                    for contrary_literal in
                    literal.contraries_and_contradictories]):
                # L-D-a: A contrary of the literal is observed, so the
                # literal cannot be in the grounded extension.
                labels.literal_labeling[literal].defended = False
        else:
            if all([not labels.rule_labeling[rule].defended
                    for rule in children[literal]]):
                # L-D-b: The literal is not observable and there is no
                # defended rule, so the literal cannot be defended.
                labels.literal_labeling[literal].defended = False
            elif any([not labels.rule_labeling[contrary_rule].unsatisfiable and
                      not labels.rule_labeling[contrary_rule].out
                      for contrary_literal in
                      literal.contraries_and_contradictories
                      for contrary_rule in children[contrary_literal]]):
                # L-D-c: The literal is not observable and there is a
                # defended or blocked rule for a contrary, so the
                # literal cannot be defended.
                labels.literal_labeling[literal].defended = False

        if iat.is_queryable(literal):
            if literal in iat.knowledge_base:
                # L-O-a: Observed literals cannot be out.
                labels.literal_labeling[literal].out = False
            elif all([any([contrary_contrary_literal in iat.knowledge_base
                           for contrary_contrary_literal in
                           contrary_literal.contraries_and_contradictories])
                      for contrary_literal in
                      literal.contraries_and_contradictories]):
                if all([not labels.rule_labeling[rule].out
                        for rule in children[literal]]):
                    # L-O-b
                    labels.literal_labeling[literal].out = False
                elif any([not labels.rule_labeling[rule].unsatisfiable and
                          not labels.rule_labeling[rule].out
                          for rule in children[literal]]):
                    # L-O-c
                    labels.literal_labeling[literal].out = False
        else:
            if all([not labels.rule_labeling[rule].out
                    for rule in children[literal]]):
                # L-O-d
                labels.literal_labeling[literal].out = False
            elif any([not labels.rule_labeling[rule].unsatisfiable and
                      not labels.rule_labeling[rule].out
                      for rule in children[literal]]):
                # L-O-e
                labels.literal_labeling[literal].out = False
        if all([not labels.rule_labeling[rule].defended and
                not labels.rule_labeling[rule].out and
                not labels.rule_labeling[rule].blocked
                for rule in children[literal]]):
            # L-O-f: There is no rule-based argument for the literal,
            # so the literal cannot be out.
            labels.literal_labeling[literal].out = False

        if iat.is_queryable(literal):
            # L-B-a: Observable literals cannot be blocked (only
            # defended or unsatisfiable).
            labels.literal_labeling[literal].blocked = False
        elif all([not labels.rule_labeling[rule].defended and
                  not labels.rule_labeling[rule].blocked
                  for rule in children[literal]]):
            # L-B-b: There is no defended or blocked rule-based argument for
            # the literal, so it cannot be blocked.
            labels.literal_labeling[literal].blocked = False
        elif all([not labels.rule_labeling[contrary_rule].blocked and
                  not labels.rule_labeling[contrary_rule].defended
                  for contrary_literal in
                  literal.contraries_and_contradictories
                  for contrary_rule in children[contrary_literal]]):
            if all([not labels.rule_labeling[rule].blocked
                    for rule in children[literal]]):
                # L-B-c: There is no rule-based counterargument that is
                # strong enough.
                labels.literal_labeling[literal].blocked = False
            elif any([not labels.rule_labeling[rule].unsatisfiable and
                      not labels.rule_labeling[rule].out and
                      not labels.rule_labeling[rule].blocked
                      for rule in children[literal]]):
                # L-B-d: There is a rule-based argument in the
                # grounded extension.
                labels.literal_labeling[literal].blocked = False

    @staticmethod
    def _color_rule(rule: DefeasibleRule, labels: StabilityLabels):
        """
        Color the Rule, that is: check, based on is children, if this Rule can
        still become unsatisfiable/defended/out/blocked.
        """
        if all([not labels.literal_labeling[literal].unsatisfiable
                for literal in rule.antecedents]):
            # R-U-a: None of the antecedents can become unsatisfiable,
            # so the rule cannot be unsatisfiable.
            labels.rule_labeling[rule].unsatisfiable = False

        if any([not labels.literal_labeling[literal].defended
                for literal in rule.antecedents]):
            # R-D-a: At least one of the antecedents cannot become defended,
            # so the rule cannot be defended.
            labels.rule_labeling[rule].defended = False

        if all([not labels.literal_labeling[literal].out
                for literal in rule.antecedents]):
            # R-O-a: None of the antecedents can become out, so the rule
            # cannot be out.
            labels.rule_labeling[rule].out = False

        if all([not labels.literal_labeling[literal].blocked
                for literal in rule.antecedents]):
            # R-B-a: None of the antecedents can become blocked, so the
            # rule cannot be blocked.
            labels.rule_labeling[rule].blocked = False
        if any([not labels.literal_labeling[literal].blocked and
                not labels.literal_labeling[literal].defended
                for literal in rule.antecedents]):
            # R-B-b: At least one of the antecedents cannot become defended
            # or blocked, so the rule cannot be blocked.
            labels.rule_labeling[rule].blocked = False
