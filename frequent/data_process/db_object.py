import sys

import pymysql
import logging
import global_config_var

logger = logging.getLogger('my_logger')


class Db(object):
    cur = None
    con = None

    def __init__(self):
        try:
            host = global_config_var.mysql_server_ip
            password = global_config_var.mysql_passwd
            user = global_config_var.mysql_user
            if host == "":
                print("mysql_server_ip cannot be empty!!", file=sys.stderr)
                exit(1)
            self.con = pymysql.connect(host=host, password=password, port=3306, user=user,
                                       charset='utf8')
            self.cur = self.con.cursor()
            logger.info("connect success!")
            self.cur.execute("use dockerfile_study")
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            logger.error("connect fail,error type:" + type(e).__name__)
            if "No route to host" in e.args[1]:
                logger.error("The ip address or the mysql server is incorrect!!")
            elif "Access denied for user" in e.args[1]:
                logger.error("The username or password is incorrect!!")
                logger.error("Please check if your mysql configuration is correct!!")
            else:
                logger.error(e.args[1])
            exit(2)
        except pymysql.Error as e:
            logger.error("throw an exception，type:" + type(e).__name__)
            exit(3)

    def __del__(self):
        if self.cur != None:
            self.cur.close()
        if self.con != None:
            self.con.close()

    def insert_all_data_to_DockerfileHash(self, l):
        try:
            sql = f'insert into dockerfile_hash values(%s,%s,%s,%s)'
            self.cur.executemany(sql, l)
            self.con.commit()

        except pymysql.DataError as e:
            error_info = e.args[1]
            index = int(error_info[error_info.rfind(" "):])
            l.pop(index - 1)
            while 1:
                try:
                    if l == []: break
                    sql = f'insert into dockerfile_hash values(%s,%s,%s,%s)'
                    self.cur.executemany(sql, l)
                    self.con.commit()
                    break
                except pymysql.DataError as e:
                    a = e.args[1]
                    index = a.rfind(" ")
                    b = a[index:]
                    l.pop(int(b) - 1)
        except:
            raise


if __name__ == "__main__":
    db = Db()
    # l=[]
    # t = ('https://github.com/docker-library/python.git', './3.10/alpine3.17/Dockerfile', 59,
    #      '5de3a27d7100f6f9d425b487d5bedfe5eb6079c4', 60, '2592ad88d5eab56e8ef1cc736153bd23eec1cf55', 'delete', 'RUN',
    #      '# " because it needs the \' around the path, and \'"\'"\' instead is 🤢', '', 90)
    # t1 = ('https://github.com/docker-library/python.git', './3.10/alpine3.17/Dockerfile', 59,
    #      '5de3a27d7100f6f9d425b487d5bedfe5eb6079c4', 60, '2592ad88d5eab56e8ef1cc736153bd23eec1cf55', 'delete', 'RUN',
    #      '#', '', 90)
    # l.append(t)
    # l.append(t)
    # l.append(t)
    # l.append(t)
    # db.insert_all_data_to_gitChange(l)
