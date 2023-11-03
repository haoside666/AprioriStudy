# -*- coding: utf-8 -*-
"""
@Time ： 2023/10/27 下午4:34
@Auth ： haoside
@File ：preprocess.py
@IDE ：PyCharm
"""

import os
import dockerfile
import standardization
import random


def createDir(dir_name):
    os.makedirs(dir_name, exist_ok=True)


def process_file(file_path):
    with open(file_path, "r") as dfh:
        try:
            parsed_dockerfile = dockerfile.parse_string(dfh.read())
            # Create a Standardization object
            standard_obj = standardization.Standardization()
            return standard_obj.standard(parsed_dockerfile)
        except:
            raise Exception("error")


def random_select_file_by_number(folder_path, number):
    file_list = os.listdir(folder_path)
    num_files = len(file_list)
    if num_files <= number:
        return file_list
    else:
        selected_files = random.sample(file_list, min(num_files, number))
        return selected_files


def random_select_file_by_percentage(folder_path, percentage):
    file_list = os.listdir(folder_path)
    num_files = len(file_list)
    if num_files <= 5:
        return file_list
    else:
        selected_files = random.sample(file_list, int(num_files * percentage))
        return selected_files


# one structure indicates that there is only one level of directory
def split_file_by_number_and_one_structure(src_dir, dst_dir, number):
    dirs = os.listdir(src_dir)
    for project_name in dirs:
        project_path = os.path.join(src_dir, project_name)
        createDir(os.path.join(dst_dir, project_name))
        selected_files = random_select_file_by_number(project_path, number)
        for filename in selected_files:
            file_path = os.path.join(project_path, filename)
            try:
                handled_file = process_file(file_path)
                with open(os.path.join(dst_dir, project_name, filename), "w") as file:
                    file.write("\n".join(handled_file))
            except Exception:
                continue
    return


def read_dockerhub_file_list_by_number(project_path, number):
    file_list = []
    for root, dirs, files in os.walk(project_path, topdown=False):
        for name in files:
            if name != "tags_time_order.json":
                file_list.append(os.path.join(root, name).replace(project_path + "/", ""))

    num_files = len(file_list)
    if num_files <= number:
        return file_list
    else:
        selected_files = random.sample(file_list, min(num_files, number))
        return selected_files


def split_file_by_number_and_multilayer_structure(src_dir, dst_dir, number):
    dirs = os.listdir(src_dir)
    for project_name in dirs:
        project_path = os.path.join(src_dir, project_name)
        createDir(os.path.join(dst_dir, project_name))

        selected_files = read_dockerhub_file_list_by_number(project_path, number)
        for file_two_name in selected_files:
            file_path = os.path.join(project_path, file_two_name)
            try:
                handled_file = process_file(file_path)
                filename = f'{os.path.dirname(file_two_name).replace("/", "##")}##Dockerfile'
                with open(os.path.join(dst_dir, project_name, filename), "w") as file:
                    file.write("\n".join(handled_file))
            except Exception:
                continue
    return


def split_file_by_percentage_and_one_structure(src_dir, dst_dir, percentage):
    dirs = os.listdir(src_dir)
    for project_name in dirs:
        project_path = os.path.join(src_dir, project_name)
        createDir(os.path.join(dst_dir, project_name))
        selected_files = random_select_file_by_percentage(project_path, percentage)
        for filename in selected_files:
            file_path = os.path.join(project_path, filename)
            try:
                handled_file = process_file(file_path)
                with open(os.path.join(dst_dir, project_name, filename), "w") as file:
                    file.write("\n".join(handled_file))
            except Exception:
                continue
    return


def preprocess_automatic_dataset():
    root_dir = "/home/haoside/Desktop/OSSSC-Team-Resource/dataset/dockerfile-dataset/dockerfile_automatic_build/dockerfile"
    save_dir = "/home/haoside/Desktop/dataset/dataset1"
    number = 5
    split_file_by_number_and_one_structure(root_dir, save_dir, number)


def preprocess_gitchange_first_dataset():
    root_dir = "/home/haoside/Desktop/OSSSC-Team-Resource/dataset/dockerfile-dataset/dockerfile-change/first/output"
    save_dir = "/home/haoside/Desktop/dataset/dataset2"
    number = 5
    split_file_by_number_and_one_structure(root_dir, save_dir, number)


def preprocess_gitchange_three_dataset():
    root_dir = "/home/haoside/Desktop/OSSSC-Team-Resource/dataset/dockerfile-dataset/dockerfile-change/three/output"
    save_dir = "/home/haoside/Desktop/dataset/dataset3"
    number = 5
    split_file_by_number_and_one_structure(root_dir, save_dir, number)


def preprocess_dockerhubchange_official_dataset():
    root_dir = "/home/haoside/Desktop/OSSSC-Team-Resource/dataset/dockerfile-dataset/dockerfile-change/second/dockerfile/library"
    save_dir = "/home/haoside/Desktop/dataset/dataset4"
    number = 5
    split_file_by_number_and_multilayer_structure(root_dir, save_dir, number)


def preprocess_dockerhubchange_github_dataset():
    root_dir = "/home/haoside/Desktop/OSSSC-Team-Resource/dataset/dockerfile-dataset/dockerfile-change/second/github"
    save_dir = "/home/haoside/Desktop/dataset/dataset5"
    number = 5
    split_file_by_number_and_multilayer_structure(root_dir, save_dir, number)


def main():
    preprocess_automatic_dataset()
    preprocess_gitchange_first_dataset()
    preprocess_gitchange_three_dataset()
    preprocess_dockerhubchange_official_dataset()
    preprocess_dockerhubchange_github_dataset()


if __name__ == "__main__":
    main()
