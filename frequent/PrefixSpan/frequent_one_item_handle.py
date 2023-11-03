import json
import sys
import os


def load_dictionary(input_dir):
    with open(os.path.join(input_dir, 'dictionary.json'), 'r') as f:
        return json.load(f)

def fun1(input_dir,output_dir):
    output_filename = os.path.join(output_dir, 'sort_output.txt')
    d = load_dictionary(input_dir)
    items = []
    with open(output_filename, encoding="utf-8") as file:
        for line in file:
            l = line.split()
            hash_value = l[0]
            number = l[1]
            str = d[hash_value]
            items.append(str + " " + number)

    with open(os.path.join(output_dir, 'processed_output.txt'), 'w', encoding="utf-8") as f:
        f.write("\n".join(items), )


if __name__ == "__main__":
    assert len(sys.argv) == 3
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    fun1(input_dir,output_dir)



