import os
import re
import uuid
import glob
import requests
import datetime
import subprocess
from lxml import etree
from gevent import monkey, pool, joinall

from logs import spider_log_info
from db.db_mysql import session
from models.spider_model import StarInfo
from db.db_redis import redis_cli, get_star_url
from utility.util_user_agent import random_user_agent
from utility.util_star_map import get_config_value, star_name_dict

# 全局取消证书验证
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# 生成随机User-Agent
headers = {
    'User-Agent': random_user_agent,
}

# monkey.patch_all()


photos_path = get_config_value('SAVE_PHOTOS', 'SAVE_PATH')
for star_name in star_name_dict.values():
    star_path = os.path.join(photos_path, star_name)
    if not os.path.exists(star_path):
        os.makedirs(star_path)

# 爬取前一天的数据
time_str = (datetime.datetime.today() - datetime.timedelta(1)).__format__('%Y.%m.%d')

data = []


# 将网页源代码构建成tree对象
def get_tree(url):
    if requests.get(url, headers=headers).status_code != 200:
        # print(url)
        spider_log_info(
            'error------request error :{}  error code:{}'.split(url, requests.get(url, headers=headers).status_code))
        return None
    html = requests.get(url, headers=headers).text
    tree = etree.HTML(html)
    return tree


def get_start_page(url_list):
    star_dict = {star_pinyin: redis_cli.llen(star_pinyin)for star_pinyin in star_name_dict.values()}
    for url in url_list:
        text = get_tree(url)
        if text is None:
            return None
        txt_list = text.xpath('//table//td[@class="title"]/a/text()')
        href_list = text.xpath('//table//td[@class="title"]/a/@href')
        for i in range(len(txt_list)):
            x = re.search(r'(?<=【).*?(?=】)', txt_list[i])
            if x is None:
                x = re.search(r'(.* .*)', txt_list[i].strip())
            if x is None:
                continue
            if len(x.group().split(' ')) != 2:
                continue
            web_time_str = x.group().split(' ')[0]
            if len(web_time_str.split('.')[0]) == 1:
                web_time_str = '0{}'.format(web_time_str)
            if len(web_time_str.split('.')[1]) == 1:
                web_time_str = '{}.0{}'.format(web_time_str.split('.')[0], web_time_str.split('.')[1])
            if x.group().split(' ')[1].split('（')[0] in star_name_dict.keys() and web_time_str in time_str:
                try:
                    # print(x.group().split(' ')[1].split('（')[0], str({time_str: href_list[i]}))
                    redis_cli.rpush(star_name_dict[x.group().split(' ')[1].split('（')[0]], str({time_str: href_list[i]}))
                except Exception as e:
                    print(e)
                    spider_log_info('error------redis error :{}'.format(e))

    return star_dict


def get_star_info(name, url):
    global data
    file_name = '{}/{}'.format(photos_path, name)
    file_num = len(glob.glob('{}/*.jpg'.format(file_name)))
    text = get_tree(url)
    if text is None:
        return None
    img_list = text.xpath('//div[@class="image-wrapper"]//img/@src')
    for i, img_url in enumerate(img_list):
        img_path = '{}/{}_{}.jpg'.format(file_name, time_str, file_num + i)
        try:
            subprocess.check_call("wget -O {} {}".format(img_path, img_url), shell=True)
            # print("{}-{}-{}-{}".format(name, time_str, img_path, img_url))
            spider_log_info('success------save success: {}-{}-{}-{}'.format(name, time_str, img_path, img_url))
            data.append({
                'id': str(uuid.uuid1()),
                'star': name,
                'release_time': time_str,
                'star_img_path': img_path,
                'star_url': img_url,
                'star_update_time': datetime.datetime.now()
            })
        except Exception as e:
            spider_log_info('error------cmd error: {}, {}'.format("wget -O {} {}".format(img_path, img_url), e))


def main():
    Pool = pool.Pool(10)
    start_url = get_config_value('STAR_HOMEPAGE', 'URL')
    start_url_list = ['{}{}'.format(start_url, i) for i in range(0, 200, 25)]
    star_dict = get_start_page(start_url_list)
    for name, index in star_dict.items():
        greenlets = [Pool.spawn(get_star_info, name, url) for url in get_star_url(name, index)]
        joinall(greenlets)

    if data:
        try:
            session.execute(StarInfo.__table__.insert(), data)
            session.commit()
            session.close()
            spider_log_info('success-----mysql save success')
        except Exception as e:

            spider_log_info('error-------mysql db save error: {}\n data: {}'.format(e, data))
    else:
        spider_log_info('None-------mysql db save None\n date: {}'.format(time_str))


if __name__ == '__main__':
    main()

