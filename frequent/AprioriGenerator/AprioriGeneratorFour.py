from AprioriGenerator.AprioriGenerator_Interface import AprioriGenerator_Interface
from datatypes.ItemEnum import ItemNumEnum, ItemOrderEnum
from typing import Tuple


# 要求频繁项有先后顺序要求，且有重复项
class AprioriGeneratorFour(AprioriGenerator_Interface):
    def init_info(self):
        self.item_num_type = ItemNumEnum.REPEAT
        self.item_order_type = ItemOrderEnum.ORDER

    def meet_find_condition(self):
        return not self.frequent_item_list_is_empty()

    def generate_candidate_k_items(self):
        self.candidate_item_list = []
        for item1 in self.frequent_item_list:
            for item2 in self.frequent_item_list:
                self.union(item1, item2)

    def generate_frequent_k_items_by_candidate_k_items(self):
        self.frequent_dict = {}
        for basket in self.data:
            for candidate in self.candidate_item_list:
                if issubset(candidate, basket):
                    self.frequent_dict_add_item(candidate)

        self.filter_dict_by_min_support()
        self.make_frequent_item_list_by_frequent_dict()
        self.add_frequent_dict()

    def union(self, item1, item2) -> None:
        if item1[:-1] == item2[:-1]:
            candidate = tuple(item1 + item2[-1:])
            self.candidate_item_list_add_item_order(candidate)


def issubset(candidate_item, data_row):
    length = len(candidate_item)
    cnt = 0
    for item in data_row:
        if item == candidate_item[cnt]:
            cnt += 1
            if cnt == length:
                return True
    return False


def union(item1, item2) -> Tuple:
    return tuple(set(item1 + item2))
