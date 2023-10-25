import json
import time
import logging
logger = logging.getLogger('my_logger')
def prefix_span(prefix, projectedDB, min_support):
    # 统计项目的频数
    counts = {}
    for sequence in projectedDB:
        for item in sequence:
            if item in counts:
                counts[item] += 1
            else:
                counts[item] = 1

    # 找出频繁项目
    frequent_items = [item for item, count in counts.items() if count >= min_support]

    for item in frequent_items:
        new_prefix = prefix + [item]
        print(f'{new_prefix} {counts[item]}')
        # logger.info(f'{new_prefix} {counts[item]}')
        # 创建新的投影数据库
        new_projectedDB = []
        for sequence in projectedDB:
            if item in sequence:
                index = sequence.index(item)
                new_projectedDB.append(sequence[index + 1:])

        # 递归调用PrefixSpan
        prefix_span(new_prefix, new_projectedDB, min_support)


def main(data, min_support):
    initLogger()
    # 数据集是一个包含序列的列表
    prefix_span([], data, min_support)

def initLogger():
    logger = logging.getLogger('my_logger')
    log_name = './output.log'

    file_handler = logging.FileHandler(filename=log_name, mode="w")
    file_handler.setFormatter(logging.Formatter('%(message)s'))
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)

if __name__ == "__main__":
    # 示例数据集
    data = [
        [1, 3, 1, 4, 2],
        [1, 2],
    ]
    # with open('./dataset1.json', 'r') as f:
    #     data = json.load(f)

    # 设置最小支持度阈值
    min_support = 2
    # 记录程序开始时间
    start_time = time.time()
    # 示例
    main(data,min_support)
    # 记录程序结束时间
    end_time = time.time()
    # 计算程序运行时间
    run_time = end_time - start_time
    # 输出程序运行时间
    print(f"程序运行时间为：{run_time}秒")
