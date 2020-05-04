# -*- coding: UTF-8 -*-
import datetime


def runtime(func):
    def wrapper():
        start_time = datetime.datetime.now()
        func()
        over_time = datetime.datetime.now()
        total_time = (over_time-start_time).total_seconds()
        print('程序{}共运行{}秒'.format(func.__name__, total_time))
    return wrapper


if __name__ == '__main__':
    pass
