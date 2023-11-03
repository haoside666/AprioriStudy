import time
import json
from collections import defaultdict
import sys
import os

def load_data(input_dir):
    # 购物篮数据集
    with open(os.path.join(input_dir, 'dataset1.json'), 'r') as f:
        data = json.load(f)
    return data




def main(input_dir,output_dir):
    # load the data
    data = load_data(input_dir)
    # set the min support number
    min_support = 1

    item_counts = defaultdict(int)
    for basket in data:
        for item in basket:
            item_counts[item] += 1

    items = list(item_counts.items())
    frequent_dict = {k: v for k, v in items if v >= min_support}

    output_file=os.path.join(output_dir, 'output.txt')
    with open(output_file, 'w') as f:
        pass
        
    with open(output_file, 'a') as f:
        for frequent_item, value in frequent_dict.items():
            print(str(frequent_item) + "  " + str(value), file=f)


if __name__ == "__main__":
    assert len(sys.argv) == 3
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    main(input_dir,output_dir)


