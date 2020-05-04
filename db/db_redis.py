import redis

from utility.util_config import get_config_value
from utility.util_star_map import star_name_dict


host = get_config_value('DB_REDIS', 'REDIS_HOST')
port = get_config_value('DB_REDIS', 'REDIS_PORT')

pool = redis.ConnectionPool(host=host, port=port, decode_responses=True)
redis_cli = redis.Redis(connection_pool=pool)


def show_or_pop_redis():
    for pinyin in star_name_dict.values():
        print(pinyin, redis_cli.llen(pinyin))
        while redis_cli.llen(pinyin):
            print(redis_cli.lpop(pinyin))


def get_star_url(name='yangmi', index=0):
    url_list = [eval(url) for url in redis_cli.lrange(name, index, redis_cli.llen(name))]
    # print(url_list)

    for index, urls in enumerate(url_list):
        # for url in urls.values():
        # print(list(urls.values())[0])
        yield list(urls.values())[0]


def show_redis_url():
    for pinyin in star_name_dict.values():
        print(pinyin, redis_cli.llen(pinyin))
        for i in get_star_url(name=pinyin):
            print(i)


if __name__ == '__main__':
    # show_or_pop_redis()
    show_redis_url()
