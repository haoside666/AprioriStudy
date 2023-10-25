import json


def load_dictionary():
    with open('./data/dictionary.json', 'r') as f:
        return json.load(f)

def fun1():
    output_filename = "../output/sort_output.txt"
    d = load_dictionary()
    items = []
    with open(output_filename, encoding="utf-8") as file:
        for line in file:
            l = line.split()
            hash_value = l[0][2:34]
            number = l[1]
            str = d[hash_value]
            items.append(str + " " + number)

    with open('../output/processed_output.txt', 'w', encoding="utf-8") as f:
        f.write("\n".join(items), )

def fun2():
    output_filename = "../output/output.log"
    d = load_dictionary()
    data = []
    with open(output_filename, encoding="utf-8") as file:
        for line in file:
            l=[]
            parts = line.rsplit(maxsplit=1)
            list_part = parts[0]
            num_part = parts[1]
            # 将列表部分转换为Python列表
            list_obj = eval(list_part)
            for item in list_obj:
                l.append(d[item])
            data.append((l,int(num_part)))
    sorted_data = sorted(data, key=lambda x: x[1])
    items=[{"number":item[1],"content":item[0]} for item in sorted_data]

    with open('../output/processed_output.json', 'w', encoding="utf-8") as f:
        json.dump(items, f)

if __name__ == "__main__":
    fun2()



