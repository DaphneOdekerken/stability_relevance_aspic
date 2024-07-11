from typing import Dict

from .stability_label import StabilityLabel
from ..stability_result import StabilityResult
from ...classes.literal import Literal
from ...classes.rule import Rule


class StabilityLabels:
    def __init__(self, literal_labeling: Dict[Literal, StabilityLabel],
                 rule_labeling: Dict[Rule, StabilityLabel]):
        self.literal_labeling = literal_labeling
        self.rule_labeling = rule_labeling

    def to_stability_result(self) -> StabilityResult:
        stability_result = StabilityResult()
        for literal, stability_label in self.literal_labeling.items():
            if stability_label.is_stable:
                lit_name = literal.s1
                if stability_label.unsatisfiable:
                    stability_result.add_to_result(lit_name, 'unsatisfiable')
                elif stability_label.defended:
                    stability_result.add_to_result(lit_name, 'defended')
                elif stability_label.out:
                    stability_result.add_to_result(lit_name, 'out')
                elif stability_label.blocked:
                    stability_result.add_to_result(lit_name, 'blocked')
        return stability_result
