import pathlib

import clingo


PATH_TO_ENCODINGS = pathlib.Path(__file__).parent / 'encodings'


class RelevanceSolver:
    def __init__(self):
        # Queryables and initial (not guessed) axioms parsed from the input.
        self.queryables = set()
        self.initial_axioms = set()
        self.topic = None

        # Clingo controls
        self.guess_control = None
        self.verify_control = None

        # Axioms found in the model of guess_control.
        self.axiom_set = set()

        # *External* axioms that guessed by guess_control and not in the input.
        self.currently_enforced_axioms = set()

        # Last new rule added to guess_control because of model by
        # verify_control.
        self.rule_out_subsets_rule = []

        # Dictionaries below store the "translation" from queryable to
        # clingo functions.
        self.queryable_to_clingo_axiom = dict()
        self.queryable_to_clingo_naxiom = dict()
        self.queryable_to_clingo_eaxiom = dict()

    def clean(self):
        for axiom_atom in self.currently_enforced_axioms:
            self.verify_control.assign_external(axiom_atom, False)
        self.axiom_set = set()
        self.currently_enforced_axioms = set()

    def _store_guessed_axioms(self, model):
        for queryable_name in self.queryables:
            axiom_atom = self.queryable_to_clingo_axiom[queryable_name]
            if model.contains(axiom_atom):
                self.axiom_set.add(queryable_name)

    def _store_rule_out_subsets_rule(self, model):
        body = []

        for a in self.queryables:
            naxiom_atom = self.queryable_to_clingo_naxiom[a]
            if model.contains(naxiom_atom):
                with self.guess_control.backend() as backend:
                    body.append(backend.add_atom(naxiom_atom))

        self.rule_out_subsets_rule = body

    def _parse_input(self, input_file):
        with open(input_file, 'r') as infile:
            text = infile.readlines()

        for line in text:
            if line.startswith('axiom'):
                self.initial_axioms.add(line.split('(')[1].split(')')[0])
            elif line.startswith('queryable'):
                self.queryables.add(line.split('(')[1].split(')')[0])
            elif line.startswith('topic'):
                self.topic = line.split('(')[1].split(')')[0]

    def _setup_clingo_relevance(self, iat_file,
                                with_preferences: bool = False):
        # Initialise guess_control.
        self.guess_control = clingo.Control()
        self.guess_control.load(iat_file)
        self.guess_control.load(str(PATH_TO_ENCODINGS / 'guess.dl'))
        self.guess_control.ground([('base', [])], context=self)

        # Initialise verify_control.
        self.verify_control = clingo.Control()
        self.verify_control.load(iat_file)
        self.verify_control.load(str(PATH_TO_ENCODINGS / 'derivable.dl'))
        if with_preferences:
            stability_file_name = 'grounded_stability_with_preferences.dl'
        else:
            stability_file_name = 'grounded_stability.dl'
        self.verify_control.load(
            str(PATH_TO_ENCODINGS / stability_file_name))
        self.verify_control.load(
            str(PATH_TO_ENCODINGS / 'relevance_externals.dl'))
        self.verify_control.load(str(PATH_TO_ENCODINGS / 'filter_status.dl'))
        self.verify_control.ground([('base', [])], context=self)

        # Store clingo functions for assuming (the absence of) axioms after
        # a guess.
        for queryable_name in self.queryables:
            self.queryable_to_clingo_axiom[queryable_name] = \
                clingo.Function('axiom', [clingo.Function(queryable_name)])
            self.queryable_to_clingo_naxiom[queryable_name] = \
                clingo.Function('naxiom', [clingo.Function(queryable_name)])
            self.queryable_to_clingo_eaxiom[queryable_name] = \
                clingo.Function('eaxiom', [clingo.Function(queryable_name)])

        # Remove assumed axioms from possible previous runs.
        self.clean()

    def relevance_all_incremental(self, input_file, prefs,
                                  status='defended'):
        # Parse input.
        self._parse_input(input_file)

        # Setup controls.
        self._setup_clingo_relevance(input_file, prefs)

        potential_queryables = \
            {q for q in self.queryables if q not in self.initial_axioms}
        relevant_queryables = set()

        topic_not_status = \
            clingo.Function(status, [clingo.Function(self.topic)])
        topic_not_status_assumption = [(topic_not_status, False)]

        while True:
            # Repeat as long as there are new completions to be guessed.
            if not self.guess_control.solve(
                    on_model=self._store_guessed_axioms).satisfiable:
                break

            # If a model was found by self.guess_control, then its axioms are
            # stored in self.axiom_set by self._store_guessed_axioms.

            # Add "newly guessed" axioms as externals to self.verify_control.
            for a in self.axiom_set:
                axiom_atom = self.queryable_to_clingo_eaxiom[a]
                if a not in self.initial_axioms:
                    self.verify_control.assign_external(axiom_atom, True)
                    self.currently_enforced_axioms.add(axiom_atom)

            # First check if the topic is *not* stable for this status.
            check_topic_not_status = self.verify_control.solve(
                on_model=self._store_rule_out_subsets_rule,
                assumptions=topic_not_status_assumption)

            # If a model was found by self.verify_control,
            # then self.rule_out_subsets_rule contains a clingo rule that
            # states that subsets of this axiom set need not be considered.

            if check_topic_not_status.satisfiable:
                # The topic is not stable for this status (so search further).
                with self.guess_control.backend() as backend:
                    backend.add_rule(head=[], body=self.rule_out_subsets_rule)
            else:
                # The topic is stable for this status.

                # Try all newly added axioms and see if they caused this
                # stability (and thus are relevant).
                queryables_in_cand = \
                    set.intersection(potential_queryables, self.axiom_set)
                for query in queryables_in_cand:
                    # Add an external atom stating that the queryable is
                    # *not* an axiom.
                    query_atom = self.queryable_to_clingo_eaxiom[query]
                    self.verify_control.assign_external(query_atom, False)

                    check_topic_not_status_without_query = \
                        self.verify_control.solve(topic_not_status_assumption)
                    if check_topic_not_status_without_query.satisfiable:
                        # Without the queryable, the topic is *not* stable for
                        # this status. Thus, the queryable is relevant.
                        relevant_queryables.add(query)
                        potential_queryables.remove(query)

                    # Put the queryable back as an external atom (as it was
                    # guessed).
                    self.verify_control.assign_external(query_atom, True)

                # No superset of the candidate needs to be considered.
                body = []
                for a in self.axiom_set:
                    with self.guess_control.backend() as backend:
                        axiom_atom = self.queryable_to_clingo_axiom[a]
                        body.append(backend.add_atom(axiom_atom))
                with self.guess_control.backend() as backend:
                    backend.add_rule(head=[], body=body)

            self.clean()

        return relevant_queryables
