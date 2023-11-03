# -*- coding: utf-8 -*-
"""
@Time ： 2023/11/2 下午10:12
@Auth ： haoside
@File ：split_by_base_image.py
@IDE ：PyCharm
"""
import os
import dockerfile
from dockerfile import Command
from shutil import copyfile


def main(basic_path):
    dirs = os.listdir(basic_path)
    d = {}
    for project_name in dirs:
        project_path = os.path.join(basic_path, project_name)
        for filename in os.listdir(project_path):
            file_path = os.path.join(project_path, filename)
            try:
                with open(file_path, "r") as dfh:
                    parsed_dockerfile = dockerfile.parse_string(dfh.read())
                    flags = False
                    for instruct in parsed_dockerfile:
                        if instruct.cmd == "FROM":
                            image_info: Command = instruct
                            flags = True
                            break
                    if not flags: continue
                    if len(image_info.value) != 0:
                        base_image = image_info.value[0].split(":")[0]
                        if base_image not in d:
                            d[base_image] = [file_path]
                        else:
                            d[base_image].append(file_path)
            except Exception:
                raise
    for item, dockerfile_paths in d.items():
        if len(dockerfile_paths) >= 50:
            project_path = os.path.join("/home/haoside/Desktop/dataset/split", item)
            os.makedirs(os.path.join("/home/haoside/Desktop/dataset/split", item))
            for dockerfile_path in dockerfile_paths:
                dst_path = os.path.join(project_path, os.path.basename(dockerfile_path))
                copyfile(dockerfile_path, dst_path)


if __name__ == "__main__":
    basic_path = "/home/haoside/Desktop/dataset/dataset_all"
    main(basic_path)
