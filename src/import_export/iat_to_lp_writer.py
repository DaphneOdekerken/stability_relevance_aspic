from typing import Optional, List

from ..classes.incomplete_argumentation_theory import \
    IncompleteArgumentationTheory
from ..classes.literal import Literal


def write_to_lp_file(
        iat: IncompleteArgumentationTheory,
        write_path: str,
        topic_literals: Optional[List[Literal]] = None):
    with open(write_path, 'w') as write_file:
        for literal in iat.argumentation_system.language:
            write_file.write(f'literal({literal.lower()}).\n')
        write_file.write('\n')

        for queryable in iat.queryables:
            write_file.write(f'queryable({queryable.s1.lower()}).\n')
        write_file.write('\n')

        for axiom in iat.knowledge_base_axioms:
            write_file.write(f'axiom({axiom.s1.lower()}).\n')
        write_file.write('\n')

        for literal_str, literal in iat.argumentation_system.language.items():
            for contrary in literal.contraries_and_contradictories:
                write_file.write(f'neg({literal_str.lower()},'
                                 f'{contrary.s1.lower()}).\n')
        write_file.write('\n')

        for rule in iat.argumentation_system.defeasible_rules:
            for antecedent in rule.antecedents:
                write_file.write(f'body({str(rule.id)},'
                                 f'{antecedent.s1.lower()}).\n')
            write_file.write(f'head({str(rule.id)},'
                             f'{rule.consequent.s1.lower()}).\n')
        write_file.write('\n')

        for (r1, r2) in iat.argumentation_system.rule_preferences.\
                preference_tuples:
            write_file.write(f'preferred({r1.id},{r2.id}).\n')
        write_file.write('\n')

        if topic_literals:
            for topic_literal in topic_literals:
                write_file.write(f'topic({topic_literal.s1.lower()}).\n')
