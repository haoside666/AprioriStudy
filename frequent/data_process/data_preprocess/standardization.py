# -*- coding: utf-8 -*-
"""
@Time ： 2023/10/27 下午7:59
@Auth ： haoside
@File ：standardization.py
@IDE ：PyCharm
"""
import re
from dockerfile import Command

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


class Standardization:
    def __handle_run(self, directive: Command):
        assert directive.sub_cmd is None
        original_cmd = directive.original.replace("RUN", "").strip()
        if original_cmd[0] == "[" and original_cmd[-1] == "]":
            return directive.original
        else:
            assert len(directive.value) == 1
            values: str = directive.value[0]
            value_list = values.split("&&")
            l = []
            for item in value_list:
                item = item.strip().replace("\n", " ")
                l.append("RUN " + re.sub(r'\s+', ' ', item))
            return "\n".join(l)

    def __path_segmentation(self, path):
        if len(path) == 2:
            srcDir = path[0]
            dstDir = path[1]
            dstDir_split = dstDir.split("/")
            if len(dstDir_split) != 1:
                dstDir_postfix = dstDir_split[-1]
                srcDir_postfix = srcDir.split("/")[-1]
                if srcDir_postfix == dstDir_postfix:
                    dstDir = dstDir[:-len(dstDir_postfix)]
            values = f'{srcDir} {dstDir}'
        else:
            values = f'{" ".join(path)}'
        return values

    def __handle_copy_or_add(self, directive: Command):
        assert directive.sub_cmd is None
        value = self.__path_segmentation(directive.value)
        return f'{directive.cmd} {value}'

    def __handle_arg(self, directive: Command):
        assert directive.sub_cmd is None
        values = []
        for item in directive.value:
            if "=" not in item:
                values.append(f'{item}=""')
            else:
                values.append(item)

        return f'{directive.cmd} {" ".join(values)}'

    def __handle_env(self, directive: Command):
        assert directive.sub_cmd is None
        value = directive.value
        length = len(value) // 2
        values = []
        for i in range(length):
            env_value=value[2 * i + 1].replace('"','')
            temp=f'="{env_value}"'
            values.append(f'{value[2 * i]}{temp}')
        return f'{directive.cmd} {" ".join(values)}'

    def __handle_default(self, directive: Command):
        return re.sub('\s+', " ", directive.original).replace("\n"," ")

    __instruct_op = {
        "RUN": __handle_run,
        'FROM': __handle_default,
        'CMD': __handle_default,
        'LABEL': __handle_default,
        'MAINTAINER': __handle_default,
        'EXPOSE': __handle_default,
        'ENV': __handle_env,
        'ADD': __handle_copy_or_add,
        'COPY': __handle_copy_or_add,
        'ENTRYPOINT': __handle_default,
        'VOLUME': __handle_default,
        'USER': __handle_default,
        'WORKDIR': __handle_default,
        'ARG': __handle_arg,
        'ONBUILD': __handle_default,
        'STOPSIGNAL': __handle_default,
        'HEALTHCHECK': __handle_default,
        'SHELL': __handle_default
    }

    def standard(self, block):
        standard_block = []
        for directive in block:
            if directive.cmd in VALID_DIRECTIVES:
                item = self.__instruct_op[directive.cmd](self, directive)
                standard_block.append(item)
            else:
                raise Exception("error")
        return standard_block
