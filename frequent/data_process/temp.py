# -*- coding: utf-8 -*-
"""
@Time ： 2023/10/18 下午1:32
@Auth ： haoside
@File ：temp.py
@IDE ：PyCharm
"""
import os
import dockerfile
import json

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

if __name__ == "__main__":
    root_dir = "/home/haoside/Desktop/OSSSC-Team-Resource/dataset/dockerfile-dataset/dockerfile_automatic_build/dockerfile"
    dirs = os.listdir(root_dir)
    items = []
    for project_name in dirs:
        project_path = os.path.join(root_dir, project_name)
        for filename in os.listdir(project_path):
            l = []
            file_path = os.path.join(project_path, filename)
            with open(file_path) as dfh:
                try:
                    parsed_dockerfile = dockerfile.parse_string(dfh.read())
                    for command in parsed_dockerfile:
                        cmd = command.cmd
                        if cmd not in VALID_DIRECTIVES:
                            raise Exception("error")
                        l.append(cmd)
                except Exception:
                    continue
            items.append(l)
    with open('/home/haoside/Desktop/dataset.json', 'w') as f:
        json.dump(items, f)
