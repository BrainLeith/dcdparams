import configparser
import json
import os
import shutil
import requests
from parsel import Selector

# headers必须要有,请求时模拟浏览器
headers = {
    'pragma': 'no-cache',
    'accept-language': 'zh-CN,zh;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'accept': '*/*',
    'cache-control': 'no-cache',
    'authority': 'www.dongchedi.com',
}
# 爬取参数的详情页
get_car_params = "https://www.dongchedi.com/auto/params-carIds-{car_id}"
# 获取车系下的车系id
get_car_series_id_url = "https://www.dongchedi.com/search?keyword={car_name}&currTab=1&city_name={city_name}&search_mode=history"
# 获取车系下的车型id
get_car_detail_url = "https://www.dongchedi.com/motor/pc/car/series/car_list?series_id={car_id}&city_name={city_name}"


def get_config(section, property_name):
    config = configparser.ConfigParser()
    config.read("config.ini", encoding="utf-8")
    return config.get(section, property_name)


def clean_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    else:
        shutil.rmtree(dir_path, ignore_errors=True)


def get_car_series_id(car_name, city_name):
    carid_url = get_car_series_id_url.format(car_name=car_name, city_name=city_name)
    response = requests.get(url=carid_url, headers=headers).text
    selector = Selector(text=response)
    car_message = selector.css('''.dcd-car-series a::attr(data-log-click)''').get()
    car_message = json.loads(car_message)
    car_series_id = car_message.get("car_series_id")
    return car_series_id


def get_car_id(car_series_id, city_name):
    car_detail_url = get_car_detail_url.format(car_id=car_series_id, city_name=city_name)
    response = requests.get(url=car_detail_url, headers=headers).json()
    online_all_list = response.get("data").get("tab_list")[0].get("data")
    car_real_id_list = []
    for car_cls in online_all_list:
        car_cls = car_cls.get("info")
        if car_cls.get("car_id") is not None:
            car_real_id_list.append(car_cls.get("car_id"))
    return car_real_id_list


def get_params(div_tag, sub_string):
    str_new = div_tag.getText(',')[len(sub_string + ","):]
    string_list = str_new.split(',')
    even_list = []
    for j in range(len(string_list)):
        if j % 2 == 0:
            even_list.append(string_list[j])
    even_list2 = []
    for j in range(len(string_list)):
        if j % 2 == 1:
            even_list2.append(string_list[j])
    text = ''
    for j in range(0, len(even_list)):
        for ii in range(0, len(even_list2)):
            if j == ii:
                text = text + (even_list[j] + even_list2[ii]) + '，'
    return text
