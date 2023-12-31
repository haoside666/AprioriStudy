# -*- coding: utf-8 -*-
"""
@Time ： 2023/10/18 下午1:32
@Auth ： haoside
@File ：handle.py
@IDE ：PyCharm
"""
import os
import dockerfile
import json
import hashlib
import time
# import logging
# from config import set_config_info
# from db_object import Db
# from DockerfileHashClass import DockerfileHash

VALID_DIRECTIVES = [
    'FROM',
    'RUN',
    'CMD',
    'LABEL',
    'MAINTAINER',
    'EXPOSE',
    'ENV',
    'ADD',
    'COPY',
    'ENTRYPOINT',
    'VOLUME',
    'USER',
    'WORKDIR',
    'ARG',
    'ONBUILD',
    'STOPSIGNAL',
    'HEALTHCHECK',
    'SHELL'
]


def md5_hash(text):
    # 创建一个md5 hash对象
    md5 = hashlib.md5()

    # 向md5对象中添加要哈希的文本
    md5.update(text.encode('utf-8'))

    # 获取哈希值并以16进制字符串的形式返回
    return md5.hexdigest()

# default method
def default_method(logger,db,data):
    root_dir = "/home/haoside/Desktop/OSSSC-Team-Resource/dataset/dockerfile-dataset/dockerfile_automatic_build/dockerfile"
    dirs = os.listdir(root_dir)
    hash_dictionary = {}
    items = []
    d = {}
    for project_name in dirs:
        d["pName"] = project_name
        record = []
        project_path = os.path.join(root_dir, project_name)
        for filename in os.listdir(project_path):
            d["fileName"] = filename
            l = []

            file_path = os.path.join(project_path, filename)
            with open(file_path) as dfh:
                try:
                    parsed_dockerfile = dockerfile.parse_string(dfh.read())
                    for command in parsed_dockerfile:
                        cmd = command.cmd
                        if cmd not in VALID_DIRECTIVES:
                            raise Exception("error")
                        original = command.original
                        original_hash = md5_hash(original)
                        hash_dictionary[original_hash] = original
                        if len(original) > 500:
                            d["content"] = original[:500]
                        else:
                            d["content"] = original
                        d["hash"] = original_hash
                        data.fill_data_by_dict(d)
                        record.append(data.data_to_tuple())
                        l.append(original_hash)
                except Exception:
                    continue
            items.append(l)
        logger.info(f"{project_name} Processing complete")
        db.insert_all_data_to_DockerfileHash(record)

    with open('./data/dataset1.json', 'w') as f:
        json.dump(items, f)

    with open('./data/dictionary.json', 'w') as f:
        json.dump(hash_dictionary, f)

# Methods of processing preprocessed data
def processed_method(logger,db,data):
    root_dir = "/home/haoside/Desktop/dataset/dataset_all"
    dirs = os.listdir(root_dir)
    hash_dictionary = {}
    items = []
    d = {}
    for project_name in dirs:
        d["pName"] = project_name
        record = []
        project_path = os.path.join(root_dir, project_name)
        for filename in os.listdir(project_path):
            d["fileName"] = filename
            l = []
            file_path = os.path.join(project_path, filename)
            with open(file_path, "r") as file:
                for line in file:
                    line=line.strip()
                    original_hash = md5_hash(line)
                    hash_dictionary[original_hash] = line
                    if len(line) > 500:
                        d["content"] = line[:500]
                    else:
                        d["content"] = line
                    d["hash"] = original_hash
                    data.fill_data_by_dict(d)
                    record.append(data.data_to_tuple())
                    l.append(original_hash)
            items.append(l)

        logger.info(f"{project_name} Processing complete")
        db.insert_all_data_to_DockerfileHash(record)

    with open('./data/dataset1.json', 'w') as f:
        json.dump(items, f)

    with open('./data/dictionary.json', 'w') as f:
        json.dump(hash_dictionary, f)


# Methods of processing preprocessed data
def processed_and_splited_method():
    root_dir = "/home/haoside/Desktop/dataset/split"
    for base_image in os.listdir(root_dir):
        project_path=os.path.join(root_dir,base_image)
        os.makedirs("data/"+base_image,exist_ok=True)
        hash_dictionary = {}
        items = []
        for filename in os.listdir(project_path):
            l = []
            file_path = os.path.join(project_path, filename)
            with open(file_path, "r") as file:
                for line in file:
                    line=line.strip()
                    original_hash = md5_hash(line)
                    hash_dictionary[original_hash] = line
                    l.append(original_hash)
                items.append(l)

        with open(f'./data/{base_image}/dataset1.json', 'w') as f:
            json.dump(items, f)

        with open(f'./data/{base_image}/dictionary.json', 'w') as f:
            json.dump(hash_dictionary, f)


def main():
    start = time.time()
    # logger = logging.getLogger('my_logger')
    # # Gets environment variable parameters
    # config_file_path = "/home/haoside/frequent/data_process/config.json"
    # # Configuring global information
    # set_config_info(config_file_path)
    # # Initialization
    # db = Db()
    # data = DockerfileHash()

    # function
    processed_and_splited_method()

    #
    end = time.time()
    print(end - start, 's')

if __name__ == "__main__":
    main()