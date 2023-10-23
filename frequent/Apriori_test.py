import time
from AprioriGenerator.AprioriGeneratorOne import AprioriGeneratorOne
from AprioriGenerator.AprioriGeneratorTwo import AprioriGeneratorTwo
from AprioriGenerator.AprioriGeneratorThree import AprioriGeneratorThree
from AprioriGenerator.AprioriGeneratorFour import AprioriGeneratorFour
import json


def load_data():
    # 购物篮数据集
    with open('dataset1.json', 'r') as f:
        data = json.load(f)
    return data


case_name_transformer_module_mapper = {
    "One": AprioriGeneratorOne,
    "Two": AprioriGeneratorTwo,
    "Three": AprioriGeneratorThree,
    "Four": AprioriGeneratorFour
}


def main():
    # load the data
    data = load_data()
    # set the min support number
    min_support = 500

    # Get the cmd_name
    case_name = "One"

    # Get the Apriori class
    apriori_class_for_case = case_name_transformer_module_mapper[case_name]

    # Initialize the Apriori object
    apriori_object = apriori_class_for_case(data, min_support)

    # Execute the frequent items algorithm
    apriori_object.frequent_items_algorithm()

    # Get the frequent dict list
    frequent_dict_list = apriori_object.get_frequent_dict_list()
    dimension = apriori_object.get_dimension()
    with open('output.txt', 'a') as f:
        for index in range(dimension):
            print(f"Frequent {index + 1}-itemsets:", file=f)
            frequent_dict = frequent_dict_list[index]
            for frequent_item, value in frequent_dict.items():
                print(str(frequent_item) + "  " + str(value), file=f)


if __name__ == "__main__":
    # 记录程序开始时间
    start_time = time.time()
    # 示例
    main()
    # 记录程序结束时间
    end_time = time.time()
    # 计算程序运行时间
    run_time = end_time - start_time
    # 输出程序运行时间
    print(f"程序运行时间为：{run_time}秒")
