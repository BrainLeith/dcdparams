import requests
import os
from utils.util import get_config


def get_car_series(offset):
    url = 'https://www.dongchedi.com/motor/brand/m/v6/select/series/?city_name=%E6%AD%A6%E6%B1%89'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
    data = {
        'offset': '{}'.format(offset),
        'limit': 30,
        'is_refresh': 1,
        'city_name': '武汉'
    }

    response = requests.post(url, headers=headers, data=data).json()
    all_cak = response['data']['series']
    car_series = ''
    for cake in all_cak:
        car_series += cake['outter_name'] + ','
    return car_series


# 获得根路径
def get_root_path():
    # 获取文件目录
    curPath = os.path.abspath(os.path.dirname(__file__))
    # 获取项目根路径，内容为当前项目的名字
    rootPath = curPath[:curPath.find('dcdparams') + len('dcdparams')]
    return rootPath


def config_car_series():
    new_string = ''
    for i in range(int(get_config('car_series_pages', 'start')), int(get_config('car_series_pages', 'end'))):
        new_string += get_car_series(i)

    new_string = new_string.rstrip(",")
    root_directory = get_root_path() + '\\' + get_config('car_series_file_name', 'name')
    with open(root_directory, "w", encoding="utf-8") as f:
        f.write(new_string)
    f.close()
