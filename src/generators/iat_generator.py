import random
from typing import Optional, List

from .layered_as_generator import LayeredArgumentationSystemGenerator
from .random_as_generator import RandomArgumentationSystemGenerator
from ..classes.argumentation_system import ArgumentationSystem
from ..classes.literal import Literal
from ..classes.incomplete_argumentation_theory import \
    IncompleteArgumentationTheory


class IncompleteArgumentationTheoryGenerator:
    def __init__(self, argumentation_system: ArgumentationSystem,
                 positive_queryable_candidates: Optional[List[Literal]] = None,
                 queryable_literal_ratio: float = 0.5,
                 knowledge_queryable_ratio: float = 0.5,
                 axiom_knowledge_ratio: float = 0.5):
        """
        Initialise the IncompleteArgumentationTheoryGenerator.

        Note: we assume that the contradiction function in the argumentation
        system only consists of negations.

        :param argumentation_system: The argumentation system on which
        this IncompleteArgumentationTheory will be based.
        :param positive_queryable_candidates: Literals that are positive and
        may be queryable.
        :param queryable_literal_ratio: Number of queryables compared to number
        of literals.
        :param knowledge_queryable_ratio: Number of knowledge base items
        compared to number of positive queryables.
        :param axiom_knowledge_ratio: Number of axioms compared to number of
        knowledge base items.
        """
        self.argumentation_system = argumentation_system

        if queryable_literal_ratio < 0 or queryable_literal_ratio > 1:
            raise ValueError('The queryable literal ratio should be between '
                             'zero and one.')
        self.queryable_literal_ratio = queryable_literal_ratio

        if knowledge_queryable_ratio < 0 or knowledge_queryable_ratio > 1:
            raise ValueError('The knowledge queryable ratio should be between '
                             'zero and one.')
        self.knowledge_queryable_ratio = knowledge_queryable_ratio

        if axiom_knowledge_ratio < 0 or axiom_knowledge_ratio > 1:
            raise ValueError('The axiom knowledge ratio should be between '
                             'zero and one.')
        self.axiom_knowledge_ratio = axiom_knowledge_ratio

        # Find the positive literals in the ArgumentationSystem.
        self.positive_literals = \
            [literal for literal_str, literal in
             self.argumentation_system.language.items() if
             not literal_str.startswith('not_')]

        if positive_queryable_candidates:
            self.positive_queryable_candidates = positive_queryable_candidates
        else:
            self.positive_queryable_candidates = self.positive_literals

        self.nr_of_positive_queryables = int(queryable_literal_ratio * len(
            self.positive_literals))
        knowledge_base_size = int(
            self.nr_of_positive_queryables * self.knowledge_queryable_ratio)
        self.axiom_size = int(knowledge_base_size * self.axiom_knowledge_ratio)
        self.ordinary_premise_size = knowledge_base_size - self.axiom_size

    def generate(self) -> IncompleteArgumentationTheory:
        # Sample the queryables from the set of literals.
        positive_queryables = random.sample(
            self.positive_queryable_candidates, self.nr_of_positive_queryables)
        negative_queryables = [
            self.argumentation_system.language['not_' + str(pos_q)]
            for pos_q in positive_queryables]
        queryables = positive_queryables + negative_queryables

        # Sample the axioms from the set of queryables, making sure that the
        # axioms are consistent.
        axioms = []
        axiom_candidates = queryables.copy()
        for _ in range(self.axiom_size - 1):
            if not axiom_candidates:
                raise ValueError('Could not construct such a large knowledge '
                                 'base given the contradictories.')
            new_axiom = random.choice(axiom_candidates)
            axioms.append(new_axiom)
            axiom_candidates.remove(new_axiom)
            for new_axiom_contrary in new_axiom.contraries_and_contradictories:
                axiom_candidates.remove(new_axiom_contrary)

        # Finally, sample the ordinary premises.
        ordinary_premise_candidates = [queryable for queryable in queryables
                                       if queryable not in axioms]
        ordinary_premises = random.sample(ordinary_premise_candidates,
                                          self.ordinary_premise_size)

        return IncompleteArgumentationTheory(
            argumentation_system=self.argumentation_system,
            queryables=queryables,
            knowledge_base_axioms=axioms,
            knowledge_base_ordinary_premises=ordinary_premises)


def generate_single_layered(nr_literals):
    nr_rules = int((nr_literals * 3) / 2)
    rule_antecedent_distribution = {1: int(nr_rules / 3),
                                    2: int(nr_rules / 3),
                                    3: int(nr_rules / 9),
                                    4: int(nr_rules / 9)}
    rules_left = nr_rules - sum(rule_antecedent_distribution.values())
    rule_antecedent_distribution[5] = rules_left

    literal_layer_distribution = {0: int((2 * nr_literals) / 3),
                                  1: int(nr_literals / 10),
                                  2: int(nr_literals / 10),
                                  3: int(nr_literals / 10)}
    literals_left = nr_literals - sum(literal_layer_distribution.values())
    literal_layer_distribution[4] = literals_left

    layered_argumentation_system_generator = \
        LayeredArgumentationSystemGenerator(
            nr_of_literals=nr_literals,
            nr_of_rules=nr_rules,
            rule_antecedent_distribution=rule_antecedent_distribution,
            literal_layer_distribution=literal_layer_distribution,
            strict_rule_ratio=0)

    # Generate the argumentation system, and keep the "layers" of literals.
    arg_sys, layered_language = \
        layered_argumentation_system_generator.generate(
            return_layered_language=True, add_rule_preferences=False)

    # Generate an incomplete argumentation theory, where only literals on the
    # first layer can be queryable.
    positive_queryable_candidates = {
        literal
        for literal in layered_language[0]
        if not literal.s1.startswith('not_') and
        arg_sys.language['not_' + literal.s1] in layered_language[0]
    }

    iat_generator = IncompleteArgumentationTheoryGenerator(
        argumentation_system=arg_sys,
        positive_queryable_candidates=list(positive_queryable_candidates),
        queryable_literal_ratio=0.5,
        knowledge_queryable_ratio=0.5,
        axiom_knowledge_ratio=1
    )
    iat = iat_generator.generate()

    topic_literal = random.choice(layered_language[4])
    return iat, topic_literal


def generate_single_random(nr_literals):
    nr_rules = int((nr_literals * 3) / 2)
    rule_antecedent_distribution = {1: int(nr_rules / 3),
                                    2: int(nr_rules / 3),
                                    3: int(nr_rules / 9),
                                    4: int(nr_rules / 9)}
    rules_left = nr_rules - sum(rule_antecedent_distribution.values())
    rule_antecedent_distribution[5] = rules_left

    random_argumentation_system_generator = \
        RandomArgumentationSystemGenerator(
            nr_literals, rule_antecedent_distribution)

    # Generate the argumentation system.
    arg_sys = random_argumentation_system_generator.generate()

    # Generate an incomplete argumentation theory.
    positive_queryable_candidates = {
        literal for literal in arg_sys.language.values()
        if not literal.s1.startswith('not_')
    }
    iat_generator = IncompleteArgumentationTheoryGenerator(
        argumentation_system=arg_sys,
        positive_queryable_candidates=list(positive_queryable_candidates),
        queryable_literal_ratio=0.5,
        knowledge_queryable_ratio=0.5,
        axiom_knowledge_ratio=1
    )
    iat = iat_generator.generate()

    topic_literal = random.choice(list(arg_sys.language.values()))
    return iat, topic_literal
