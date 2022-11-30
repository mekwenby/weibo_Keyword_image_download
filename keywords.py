import datetime
import os
import sys
import time

import wget
from lxml import etree
from selenium import webdriver
from selenium.webdriver import ChromeOptions

import Mek_master as Master




class Counter():  # 下载计数
    def __init__(self):
        self.good = 0
        self.retry = 0
        self.existence = 0

    def add_doog(self):
        self.good += 1

    def add_retry(self):
        self.retry += 1

    def add_existence(self):
        self.existence += 1

    def __str__(self):
        return f'已下载：{self.good} 失败：{self.retry} 已存在：{self.existence}'


counter = Counter()


def download(url, key_path,path = 'Download'):  # 执行下载的函数
    path = os.path.join(path, key_path)

    url = url
    new_i2 = url.replace('thumb150', 'large')

    new_i3 = new_i2.replace('orj360', 'large')
    new_i4 = new_i3.replace('https://wx', 'https://ww')
    if not os.path.exists(path):
        os.makedirs(path)

    # 获取文件名
    file_name = wget.filename_from_url(new_i4)
    print('开始下载', file_name)
    if not os.path.exists(os.path.join(path, file_name)):  # 判断文件是否存在，不存在就下载
        try:
            wget.download(url=new_i4, out=os.path.join(path, file_name))
            counter.add()

        except:
            print('失败', new_i4)
            counter.add_retry()
    else:
        print('已存在', file_name)
        counter.add_existence()
    print(counter)


class Keyword():

    # 浏览器控制脚本selenium的使用
    # 初始化浏览器对象
    def __init__(self):
        # 设置爬取时间段，默认为近一周
        self.start_date = (datetime.datetime.now() + datetime.timedelta(days=-7)).strftime('%Y-%m-%d')
        self.end_date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.key = None
        # 获取登陆系统的用户名
        self.name = os.getlogin()
        options = ChromeOptions()
        options.add_argument(rf'user-data-dir=C:\Users\{self.name}\AppData\Local\Google\Chrome\User Data')
        # 启用无头模式,不显示GUI
        # options.add_argument('--hadless')
        # options.add_argument('--disable-gpu')
        self.Chrome = webdriver.Chrome(executable_path='driver/chromedriver.exe', options=options)

        self.name = 'https://s.weibo.com/'

        self.Chrome.get(self.name)
        time.sleep(6)

    def build_tasks(self, key):  # 构建用于爬取的url
        key = key.replace('#', '')
        key = key.replace('#', '')
        self.key = key
        # 返回url
        return f'weibo?q=%23{key}%23&scope=ori&suball=1&timescope=custom%3A{self.start_date}-0%3A{self.end_date}-0&page=2'

    def main(self, search):

        # 发起请求
        url = self.name + search
        print(url)
        # Edge.get('www.baidu.com')
        self.Chrome.get(url)

        time.sleep(1)

        # 获得网页源代码
        html_code = self.Chrome.page_source
        Master.write_file('default.html', html_code)
        html_e = etree.HTML(html_code)

        self.next = html_e.xpath('//*[@id="pl_feedlist_index"]/div[5]/div/a[2]/@href')
        # 提取微博正文
        weibo_text = html_e.xpath('//*[@id="pl_feedlist_index"]/div[4]/div')

        for weibo in weibo_text:

            # wid

            # 发表时间

            # 正文

            #

            # print(weibo.xpath('./div/div[1]/div[2]/div[2]/a[1]/text()')[0])
            # 提取图片链接
            images = weibo.xpath('./div/div[1]/div[2]/div[3]/div/ul/li')
            for pic in images:
                # print(pic.xpath('./@action-data'))
                pics = pic.xpath('./img/@src')
                if len(pics) > 0:  # 判断是否为空列表
                    download(url=pics[0],key_path=self.key)  # 开始下载

                li_tag = etree.tostring(pic, encoding='utf-8').decode()
                # print(li_tag)

        if self.next != []:
            self.main(self.next[0])
        else:
            print('...end...')

    def exit(self):
        self.Chrome.quit()  # 退出
        sys.exit()
