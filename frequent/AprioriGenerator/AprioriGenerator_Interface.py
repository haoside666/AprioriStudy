from datatypes.ItemEnum import ItemNumEnum, ItemOrderEnum
from abc import ABC, abstractmethod
from typing import List, Tuple, Dict


class AprioriGenerator_Interface(ABC):
    def __init__(self, data, min_support=500):
        self.data = data
        self.min_support = min_support
        self.frequent_item_list: List[Tuple] = []
        self.candidate_item_list: List[Tuple] = []
        self.frequent_dict_list: List[Dict[Tuple, int]] = []
        self.frequent_dict: Dict[Tuple, int] = {}
        self.item_num_type: ItemNumEnum = ItemNumEnum.NOT_REPEAT
        self.item_order_type: ItemOrderEnum = ItemOrderEnum.DISORDER
        self.dimension = 0

    def init_info(self):
        pass

    def generate_frequent_1_items(self):
        for basket in self.data:
            for item in basket:
                self.frequent_dict_add_item((item,))

        self.filter_dict_by_min_support()
        self.make_frequent_item_list_by_frequent_dict()
        self.add_frequent_dict()

    # meet可以解释为满足或符合
    def meet_find_condition(self):
        pass

    def generate_candidate_k_items(self):
        pass

    def generate_frequent_k_items_by_candidate_k_items(self):
        pass

    def frequent_items_algorithm(self):
        self.init_info()
        self.generate_frequent_1_items()
        while self.meet_find_condition():
            self.generate_candidate_k_items()
            self.generate_frequent_k_items_by_candidate_k_items()
            self.dimension += 1

    def get_dimension(self):
        return self.dimension

    def get_frequent_dict_list(self):
        return self.frequent_dict_list

    # frequent_dict related methods
    def add_frequent_dict(self):
        self.frequent_dict_list.append(self.frequent_dict)

    def frequent_dict_add_item(self, item):
        if item not in self.frequent_dict:
            self.frequent_dict[item] = 1
        else:
            self.frequent_dict[item] += 1

    def filter_dict_by_min_support(self):
        items = list(self.frequent_dict.items())
        self.frequent_dict = {k: v for k, v in items if v >= self.min_support}

    # frequent_item_list related methods
    def frequent_item_list_is_empty(self):
        return len(self.frequent_item_list) == 0

    def make_frequent_item_list_by_frequent_dict(self):
        frequent_item_list = []
        for item, number in self.frequent_dict.items():
            frequent_item_list.append(item)
        self.frequent_item_list = frequent_item_list

    # candidate_item_list related methods
    def candidate_item_list_add_item_not_order(self,item):
        if item not in self.candidate_item_list:
            self.candidate_item_list.append(item)

    def candidate_item_list_add_item_order(self,item):
        self.candidate_item_list.append(item)