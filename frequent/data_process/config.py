import json
import logging
import datetime
import sys
import global_config_var
import os

logger = logging.getLogger('my_logger')
# Supported configuration list
SUPPORTED_CONF = [
    'LOGS_PATH',
    'LOG_LEVEL',
    'OUTPUT_TO_TERMINAL',
    'MYSQL_SERVER_IP',
    'MYSQL_USER',
    'MYSQL_PASSWD'
]


def init_log(log_level):
    if log_level == "DEBUG":
        level = logging.DEBUG
    elif log_level == "INFO":
        level = logging.INFO
    elif log_level == "WARNING":
        level = logging.WARNING
    elif log_level == "ERROR":
        level = logging.ERROR
    else:
        print(f"Unrecognized log level: {log_level}", file=sys.stderr)
        exit(12)
    if global_config_var.output_to_terminal:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
        logger.setLevel(level)
        logger.addHandler(console_handler)
    else:
        times = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_name = '{}/{}.log'.format(global_config_var.logs_path, times)
        file_handler = logging.FileHandler(filename=log_name,mode="w")
        file_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
        logger.setLevel(level)
        logger.addHandler(file_handler)


def init_resources():
    try:
        if not os.path.exists(global_config_var.logs_path):
            os.makedirs(global_config_var.logs_path)
        init_log(global_config_var.log_level)
    except PermissionError as e:
        print(f"create dir:{e.filename} fail,because Permission denied",file=sys.stderr)
        exit(13)
    except:
        exit(14)


def check_config_dict(config_dict):
    for key in config_dict.keys():
        if key not in SUPPORTED_CONF:
            print(f"Unsupported configuration information fields: {key}", file=sys.stderr)
            exit(4)


def standardized(config_dict):
    return dict(zip([*map(lambda x: x.upper(), config_dict.keys())], config_dict.values()))


def parse_config_info(config_file_path):
    try:
        with open(config_file_path, "r") as file:
            data = file.read()
        config_dict = standardized(json.loads(data))
        check_config_dict(config_dict)
        for item in SUPPORTED_CONF:
            if item == "LOGS_PATH":
                if item in config_dict:
                    global_config_var.logs_path = config_dict[item][:-1] if config_dict[item][-1] == "/" else \
                    config_dict[item]
                else:
                    print(f"--Please set LOGS_PATH--", file=sys.stderr)
                    exit(7)
            elif item == "LOG_LEVEL":
                if item in config_dict:
                    global_config_var.log_level = config_dict[item].upper()
                else:
                    global_config_var.log_level = "INFO"
            elif item == "OUTPUT_TO_TERMINAL":
                if item in config_dict:
                    output_to_terminal = config_dict[item].upper()
                    if output_to_terminal=="TRUE":
                        global_config_var.output_to_terminal=True
                    elif output_to_terminal=="FALSE":
                        global_config_var.output_to_terminal=False
                    else:
                        print(f'--Please set OUTPUT_TO_TERMINAL "FALSE" or "TRUE"--', file=sys.stderr)
                        exit(8)
                else:
                    global_config_var.output_to_terminal = False
            elif item == "MYSQL_SERVER_IP":
                if item in config_dict:
                    global_config_var.mysql_server_ip = config_dict[item]
                else:
                    print(f"--Please set MYSQL_SERVER_IP--", file=sys.stderr)
                    exit(9)
            elif item == "MYSQL_USER":
                if item in config_dict:
                    global_config_var.mysql_user = config_dict[item]
                else:
                    print(f"--Please set MYSQL_USER--", file=sys.stderr)
                    exit(10)
            elif item == "MYSQL_PASSWD":
                if item in config_dict:
                    global_config_var.mysql_passwd = config_dict[item]
                else:
                    print(f"--Please set MYSQL_PASSWD--", file=sys.stderr)
                    exit(11)
        return

    except FileNotFoundError as e:
        print("ERROR: Configuration information path does not exist!!", file=sys.stderr)
        exit(1)
    except json.JSONDecodeError as e:
        print("ERROR: json configuration information format error!!", file=sys.stderr)
        print(e.args[0], file=sys.stderr)
        exit(2)
    except:
        exit(3)


def set_config_info(config_file_path):
    parse_config_info(config_file_path)
    init_resources()
    logger.info('Starting the application')
    logger.info("Initialization of the resource was successful!!")


if __name__ == "__main__":
    config_file_path = "config.json"
    set_config_info(config_file_path)
