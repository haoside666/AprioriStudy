from util import standard_str
from typing import Tuple


class FrequentItem:
    def __init__(self, frequent_item: Tuple):
        self.frequent_item = frequent_item

    def __str__(self):
        return standard_str(self)

    def __eq__(self, other):
        return self.frequent_item == other.frequent_item

    def __hash__(self):
        return hash(self.frequent_item)

    def length(self):
        return len(self.frequent_item)
