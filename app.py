import logging
import threading
import time
import psycopg2
import requests
from bs4 import BeautifulSoup
from utils.car_series import config_car_series
from utils.dbUtil import save_to_db
from utils.util import get_car_params, headers, get_params, clean_dir, get_car_series_id, get_car_id, get_config


def get_pool():
    return psycopg2.pool.SimpleConnectionPool(1, 20, database="mine", user="postgres", password="postgres",
                                              host="localhost", port="5432")


class MyThread(threading.Thread):
    def __init__(self, name, car_id, pool):
        threading.Thread.__init__(self)
        self.name = name
        self.car_id = car_id
        self.pool = pool

    def run(self):
        car_detail = get_car_params.format(car_id=self.car_id)
        res_params = requests.get(url=car_detail, headers=headers)
        soup = BeautifulSoup(res_params.text, 'lxml')
        name = soup.find('a', class_='cell_car__28WzZ line-2').text
        logging.info('正在爬取：' + name + '的参数......')
        divs = soup.findAll('div', class_='table_root__14vH_')
        str_array = ['基本信息', '车身', '发动机', '变速箱', '底盘/转向', '车轮/制动']
        text_out = ''
        for div in divs:
            for iii in str_array:
                if div.text.startswith(iii):
                    text_out += get_params(div, iii)
        logging.info(name + '爬取完成,正在保存txt文档......')
        with open(get_config('save_dir', 'dir') + "\\" + name + ".txt", "w", encoding="utf-8") as f:
            f.write(text_out.rstrip(","))
        if get_config('save_db', 'save') == 'true':
            save_to_db(self.pool, name, text_out.rstrip(","))
        logging.info(name + '.txt文档,保存完成！')


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        level=logging.DEBUG)
    logging.info('欢迎使用懂车帝爬虫程序！')
    start_time = time.time()
    car_series_id_list = []
    logging.info('正在读取配置文件......')
    clean_dir(get_config('save_dir', 'dir'))
    if not get_config('is_auto', 'auto'):
        car_type_list = get_config('car_series', 'series').split(",")
    else:
        config_car_series()
        with open(get_config('car_series_file_name', 'name'), 'r', encoding="utf-8") as f:
            content = f.read()
        car_type_list = content.split(",")
    logging.info('读取到车系列：' + ''.join(car_type_list))
    # 获取连接池
    if get_config('save_db', 'save') == 'true':
        pool = get_pool()
        logging.info('数据库连接池创建成功！')
    else:
        pool = None
    threads = []
    for i in car_type_list:
        car_series_id_list.append(get_car_series_id(i, "南京"))
        for n in car_series_id_list:
            for kk in get_car_id(n, "南京"):
                thread = MyThread(name=kk, car_id=kk, pool=pool)
                threads.append(thread)
                thread.start()
    for thread in threads:
        thread.join()
    logging.info('所有车系列参数爬取完成！')
    if get_config('save_db', 'save') == 'true':
        # 关闭连接池
        pool.closeall()
        logging.info('数据库连接池已关闭！')
    end_time = time.time()  # 程序结束时间
    run_time = end_time - start_time  # 程序的运行时间，单位为秒
    logging.info('程序运行总消耗时间：' + str(round(run_time, 2)) + '秒')
