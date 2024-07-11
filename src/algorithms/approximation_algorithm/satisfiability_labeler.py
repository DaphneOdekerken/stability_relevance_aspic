from .stability_label import StabilityLabel
from .stability_labels import StabilityLabels
from ...classes.incomplete_argumentation_theory import \
    IncompleteArgumentationTheory


class SatisfiabilityLabeler:
    def __init__(self):
        pass

    @staticmethod
    def _preprocess_visit(rule, labels):
        if labels.rule_labeling[rule].defended:
            return False
        if all([labels.literal_labeling[literal].defended
                for literal in rule.antecedents]):
            labels.rule_labeling[rule] = StabilityLabel(True, True, True, True)
            labels.literal_labeling[rule.consequent] = StabilityLabel(
                True, True, True, True)
            return True
        return False

    def solve_stability(self, iat: IncompleteArgumentationTheory) -> \
            StabilityLabels:
        labels = StabilityLabels(dict(), dict())

        for literal in iat.argumentation_system.\
                language.values():
            if iat.is_queryable(literal) and \
                    all([contrary not in iat.knowledge_base
                        for contrary in
                         literal.contraries_and_contradictories]):
                labels.literal_labeling[literal] = StabilityLabel(
                    True, True, True, True)
            else:
                labels.literal_labeling[literal] = StabilityLabel(
                    True, False, False, False)

        for rule in iat.argumentation_system.defeasible_rules:
            labels.rule_labeling[rule] = StabilityLabel(
                True, False, False, False)

        label_added = True
        while label_added:
            label_added = False
            for rule in iat.argumentation_system.defeasible_rules:
                label_added = \
                    self._preprocess_visit(rule, labels) or label_added

        return labels
