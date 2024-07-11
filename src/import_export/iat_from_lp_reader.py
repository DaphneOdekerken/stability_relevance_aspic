from ..classes.argumentation_system import ArgumentationSystem
from ..classes.defeasible_rule import DefeasibleRule
from ..classes.literal import Literal
from ..classes.preference_preorder import PreferencePreorder
from ..classes.incomplete_argumentation_theory import \
    IncompleteArgumentationTheory


def read_from_lp_file(file_path: str) -> IncompleteArgumentationTheory:
    literal_strs = []
    queryable_strs = []
    axiom_strs = []
    defeasible_rule_bodies = []
    defeasible_rule_heads = []
    contradiction_pairs = []
    preferred_pairs = []

    reader = open(file_path, 'r')
    for line in reader:
        if line.startswith('literal'):
            literal_strs.append(line.split(
                '(', 1)[1].split(')', 1)[0])
        if line.startswith('queryable'):
            queryable_strs.append(line.split(
                '(', 1)[1].split(')', 1)[0])
        if line.startswith('axiom'):
            axiom_strs.append(line.split('(', 1)[1].split(')', 1)[0])
        if line.startswith('body'):
            defeasible_rule_bodies.append((line.split(
                '(', 1)[1].split(')', 1)[0]).split(',', 1))
        if line.startswith('head'):
            defeasible_rule_heads.append((line.split(
                '(', 1)[1].split(')', 1)[0]).split(',', 1))
        if line.startswith('neg'):
            contradiction_pairs.append((line.split(
                '(', 1)[1].split(')', 1)[0]).split(',', 1))
        if line.startswith('preferred'):
            preferred_pairs.append((line.split(
                '(', 1)[1].split(')', 1)[0]).split(',', 1))
    reader.close()

    language = {lit_str: Literal(lit_str) for lit_str in literal_strs}

    contraries_and_contradictories = \
        {lit_str: set() for lit_str in literal_strs}
    for pos, neg in contradiction_pairs:
        contraries_and_contradictories[pos].add(language[neg])

    defeasible_rules = []
    for rule_nr, rule_head in defeasible_rule_heads:
        rule_antecedents = [
            rule_body_literal
            for rule_body_nr, rule_body_literal in defeasible_rule_bodies
            if rule_body_nr == rule_nr]
        defeasible_rule = DefeasibleRule(
            rule_nr, {language[ant_str] for ant_str in rule_antecedents},
            language[rule_head])
        defeasible_rules.append(defeasible_rule)

    def_rules_lookup = {defeasible_rule.id: defeasible_rule
                        for defeasible_rule in defeasible_rules}
    preference_preorder = PreferencePreorder(
        [(def_rules_lookup[rule_a], def_rules_lookup[rule_b])
         for rule_a, rule_b in preferred_pairs])

    argumentation_system = ArgumentationSystem(
        language=language,
        contraries_and_contradictories=contraries_and_contradictories,
        strict_rules=[], defeasible_rules=defeasible_rules,
        defeasible_rule_preferences=preference_preorder,
        add_defeasible_rule_literals=False)

    queryables = [language[queryable] for queryable in queryable_strs]
    knowledge_base_axioms = [language[axiom_str] for axiom_str in axiom_strs]

    return IncompleteArgumentationTheory(
        argumentation_system=argumentation_system,
        queryables=queryables,
        knowledge_base_axioms=knowledge_base_axioms,
        knowledge_base_ordinary_premises=[],
        ordinary_premise_preferences=None
    )
