from util import standard_eq, standard_str
from typing import Tuple

class CandidateItem:
    def __init__(self, candidate_item: Tuple):
        self.candidate_item = candidate_item

    def __str__(self):
        return standard_str(self)

    def __eq__(self, other):
        return standard_eq(self, other)

    def length(self):
        return len(self.candidate_item)






