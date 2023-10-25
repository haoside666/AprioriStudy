from mlxtend.frequent_patterns import fpgrowth
import pandas as pd

# 创建一个购物篮数据集
data = pd.DataFrame({
    'Transaction': ['T1', 'T2', 'T3', 'T4', 'T5'],
    'Items': [
        '牛奶, 面包, 鸡蛋',
        '面包, 饼干',
        '牛奶, 饼干',
        '牛奶, 面包, 饼干',
        '牛奶, 面包, 鸡蛋'
    ]
})
print(data)
# 数据预处理：将项集拆分为单独的项，并将其编码为0和1
data['Items'] = data['Items'].str.split(', ')
print(data)

data_encoded=pd.get_dummies(data['Items'].apply(pd.Series).stack()).groupby(level=0).sum()
data_encoded.to_csv('example.csv')
print(data_encoded)

# 使用FP-Growth算法来找出频繁项集
frequent_itemsets = fpgrowth(data_encoded, min_support=0.2, use_colnames=True,max_len=3)

print(frequent_itemsets)
