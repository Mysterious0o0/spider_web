import base64
import binascii
from pypinyin import pinyin, NORMAL
from utility.util_config import get_config_value


# 不带声调的转换(style=pypinyin.NORMAL)
def my_pinyin(word):
    s = ''
    for i in pinyin(word, style=NORMAL):
        s += ''.join(i)
    return s


def star_name_to_pinyin():
    star_list = get_config_value('STAR_INFO', 'STAR_LIST').split(',')
    name_dict = {}
    pinyin_dict = {}
    for name in star_list:
        name_dict[name] = my_pinyin(name)
        pinyin_dict[my_pinyin(name)] = name

    return name_dict, pinyin_dict


star_name_dict, star_pinyin_dict = star_name_to_pinyin()


def encode_name(name):
    return bytes.decode(base64.b64encode(binascii.b2a_hex(name.encode())))


def decode_name(name_str):
    return binascii.a2b_hex(base64.b64decode(name_str)).decode()


if __name__ == '__main__':
    # print(star_name_to_pinyin())
    print(encode_name('杨幂'))
    print(decode_name('ZTY5ZGE4ZTViOTgy'))
