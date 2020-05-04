# -*- coding: UTF-8 -*-
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from utility.util_config import get_config_value


db = get_config_value('DB_MYSQL_DATA', 'DB')
host = get_config_value('DB_MYSQL_DATA', 'HOST')
port = get_config_value('DB_MYSQL_DATA', 'PORT')
db_type = get_config_value('DB_MYSQL_DATA', 'DB_TYPE')
username = get_config_value('DB_MYSQL_DATA', 'USERNAME')
password = get_config_value('DB_MYSQL_DATA', 'PASSWORD')

mysql_string = 'mysql+{}://{}:{}@{}:{}/{}?charset=utf8mb4'.format(db_type, username, password, host, port, db)
mysql_engine = create_engine(mysql_string, echo=True)

"""

def get_engine():
    "创建数据库连接引擎,通过引擎可以直接操作sql语句"
    # create_engine的参数依次为: 数据库类型名、用户名、密码、IP、端口、数据库名
    # 'oracle://indicator:indicator@18.1.34.11/testdb11?charset=utf8'
    # 'mysql+mysqldb://root:123@localhost/ooxx?charset=utf8'
    # mysql+pymysql://root:@ROOT_root_123/blog
    mysql_string = 'mysql+{}://{}:{}@{}:{}/{}?charset=utf8mb4'.format(db_type, username, password, host, port, db)
    mysql_engine = create_engine(mysql_string, echo=True)
    return mysql_engine
"""


def create_session(engine):
    """创建项目和数据库之间的会话对象, 打开会话, 就可以通过session用sql语句操作数据库"""
    db_session = sessionmaker(bind=engine)
    _session = db_session()
    return _session


# engine = get_engine()
session = create_session(mysql_engine)


if __name__ == '__main__':
    pass