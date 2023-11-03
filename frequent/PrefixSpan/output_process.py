import json
import sys
import os


def load_dictionary(input_dir):
    with open(os.path.join(input_dir, 'dictionary.json'), 'r') as f:
        return json.load(f)

def fun1(number,input_dir,output_dir):
    output_filename = os.path.join(output_dir, 'output.log')
    d = load_dictionary(input_dir)
    data = []
    length=int(number)-1
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
    items=[{"number":item[1],"proportions":item[1]/length,"content":item[0]} for item in sorted_data]

    with open(os.path.join(output_dir, 'processed_output.json'), 'w', encoding="utf-8") as f:
        json.dump(items, f)

if __name__ == "__main__":
    assert len(sys.argv) == 4
    number=sys.argv[1]
    input_dir = sys.argv[2]
    output_dir = sys.argv[3]
    print(f"number:{number}")
    fun1(number,input_dir,output_dir)



