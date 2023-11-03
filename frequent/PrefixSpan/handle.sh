#/bin/bash
# get frequent one items info


intput_dir="./data/ubuntu"
output_dir="./output/ubuntu"
min_sopprt="50"
mkdir -p $output_dir


echo "----------------------------------------------------"
echo "get frequent one items info begin"
python3 get_frequent_one_items.py $intput_dir $output_dir
sort -k2 -n $output_dir/output.txt>$output_dir/sort_output.txt
python3 frequent_one_item_handle.py $intput_dir $output_dir

echo "get frequent one items info Finished processing"

echo "----------------------------------------------------"
number=$(grep -o '\[' dataset1.json |wc -l)

# get all frequent items info
python3 prefix_test.py $intput_dir $output_dir $min_sopprt
echo "python3 prefix_test.py Finished processing"


python3 output_process.py $number $intput_dir $output_dir
echo "python3 output_process.py Finished processing"
cat $output_dir/processed_output.json|jq>$output_dir/processed_output_by_jq.json
