from typing import List, Optional, Union

from .argumentation_system import ArgumentationSystem
from .literal import Literal
from .preference_preorder import PreferencePreorder


class IncompleteArgumentationTheory:
    """
    An IncompleteArgumentationTheory consists of an ArgumentationSystem, a
    knowledge base and a set of queryables.
    By adding queryables, or their negations, to the knowledge base, future
    ArgumentationTheories can be obtained.
    """

    def __init__(
            self, argumentation_system: ArgumentationSystem,
            queryables: List[Literal],
            knowledge_base_axioms: List[Literal],
            knowledge_base_ordinary_premises: List[Literal],
            ordinary_premise_preferences: Optional[PreferencePreorder] =
            None):
        self._argumentation_system = argumentation_system
        self._queryables = sorted(queryables)
        self._knowledge_base_axioms = sorted(knowledge_base_axioms)
        self._knowledge_base_ordinary_premises = sorted(
            knowledge_base_ordinary_premises)

        self._is_queryable_dict = {
            lit_str: False
            for lit_str in self.argumentation_system.language.keys()}
        for queryable in self._queryables:
            self._is_queryable_dict[queryable.s1] = True

        # Rule preferences
        if ordinary_premise_preferences:
            self.ordinary_premise_preferences = ordinary_premise_preferences
        else:
            self.ordinary_premise_preferences = \
                PreferencePreorder.create_reflexive_preorder(
                    self._knowledge_base_ordinary_premises)

    @property
    def argumentation_system(self):
        return self._argumentation_system

    @property
    def queryables(self):
        return self._queryables

    def is_queryable(self, literal: Union[Literal, str]):
        if isinstance(literal, str):
            return self._is_queryable_dict[literal]
        return self._is_queryable_dict[literal.s1]

    @property
    def knowledge_base(self):
        return self._knowledge_base_axioms + \
            self._knowledge_base_ordinary_premises

    @property
    def knowledge_base_axioms(self):
        return self._knowledge_base_axioms

    @property
    def knowledge_base_ordinary_premises(self):
        return self._knowledge_base_ordinary_premises

    def __eq__(self, other):
        return isinstance(other, IncompleteArgumentationTheory) and \
            self.argumentation_system == other.argumentation_system and \
            self.queryables == other.queryables and \
            self.knowledge_base_axioms == other.knowledge_base_axioms and \
            self.knowledge_base_ordinary_premises == other.\
            knowledge_base_ordinary_premises and \
            self.ordinary_premise_preferences == other.\
            ordinary_premise_preferences
