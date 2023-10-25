from util import standard_eq, standard_str
from datatypes.FrequentItem import FrequentItem
from typing import Dict


class FrequentDict:
    def __init__(self, frequent_dict: Dict[FrequentItem, int] = {}):
        self.frequent_dict = frequent_dict

    def __str__(self):
        return standard_str(self)

    def __eq__(self, other):
        return standard_eq(self, other)

    def add_item(self, item):
        if item not in self.frequent_dict:
            self.frequent_dict[item] = 1
        else:
            self.frequent_dict[item] += 1

    def filter_dict_by_min_support(self, min_support):
        for item, number in self.frequent_dict.items():
            if number < min_support:
                self.frequent_dict.pop(item)

    def return_frequent_item_list(self):
        frequent_item_list=[]
        for item,number in self.frequent_dict.items():
            frequent_item_list.append(item)
        return frequent_item_list
