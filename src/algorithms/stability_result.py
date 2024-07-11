class StabilityResult:
    def __init__(self):
        self.stable_unsatisfiable = set()
        self.stable_defended = set()
        self.stable_out = set()
        self.stable_blocked = set()

    def add_to_result(self, literal_name: str, label: str):
        if label == 'unsatisfiable':
            self.stable_unsatisfiable.add(literal_name)
        elif label == 'defended':
            self.stable_defended.add(literal_name)
        elif label == 'out':
            self.stable_out.add(literal_name)
        elif label == 'blocked':
            self.stable_blocked.add(literal_name)
        else:
            raise NotImplementedError('This label is not known.')

    def __str__(self):
        return f'Unsatisfiable: {self.stable_unsatisfiable} \n' \
               f'Defended:      {self.stable_defended} \n' \
               f'Out:           {self.stable_out} \n' \
               f'Blocked:       {self.stable_blocked}'

    def nr_stable(self):
        return len(self.stable_unsatisfiable) + len(self.stable_defended) + \
            len(self.stable_out) + len(self.stable_blocked)

    def __eq__(self, other):
        return self.stable_unsatisfiable == other.stable_unsatisfiable and \
            self.stable_defended == other.stable_defended and \
            self.stable_out == other.stable_out and \
            self.stable_blocked == other.stable_blocked

    def is_subset_of(self, other):
        return self.stable_unsatisfiable.issubset(
            other.stable_unsatisfiable) and self.stable_defended.issubset(
            other.stable_defended) and self.stable_out.issubset(
            other.stable_out) and self.stable_blocked.issubset(
            other.stable_blocked)
