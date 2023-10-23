from AprioriGenerator.AprioriGenerator_Interface import AprioriGenerator_Interface
from datatypes.ItemEnum import ItemNumEnum, ItemOrderEnum
from typing import Tuple


# 情况一:频繁项中没有重复项,且无序
class AprioriGeneratorOne(AprioriGenerator_Interface):
    def init_info(self):
        self.item_num_type = ItemNumEnum.NOT_REPEAT
        self.item_order_type = ItemOrderEnum.DISORDER

    def meet_find_condition(self):
        return not self.frequent_item_list_is_empty()

    def generate_candidate_k_items(self):
        self.candidate_item_list = []
        for item1 in self.frequent_item_list:
            for item2 in self.frequent_item_list:
                if item1 != item2:
                    self.union(item1,item2)
                    # candidate = union(item1, item2)
                    # if len(candidate) == len(item1) + 1:
                    #     list_add_item_not_order(candidate, self.candidate_item_list)

    def generate_frequent_k_items_by_candidate_k_items(self):
        self.frequent_dict = {}
        for basket in self.data:
            for candidate in self.candidate_item_list:
                if issubset(candidate, basket):
                    self.frequent_dict_add_item(candidate)

        self.filter_dict_by_min_support()
        self.make_frequent_item_list_by_frequent_dict()
        self.add_frequent_dict()

    def union(self,item1, item2) -> None:
        if item1[:-1] == item2[:-1]:
            candidate = tuple(sorted(item1 + item2[-1:]))
            self.candidate_item_list_add_item_not_order(candidate)


def issubset(candidate_item, data_row):
    return set(candidate_item).issubset(set(data_row))

def union(item1, item2) -> Tuple:
    return tuple(sorted(set(item1) | set(item2)))

