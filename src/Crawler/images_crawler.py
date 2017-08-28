# -*- coding:utf-8 -*-

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from multiprocessing import Pool, Value
import os

DIR = 'logos'
class ImagesCrawler(object):
    def __init__(self, url_base, debug=False):
        self.url_base = url_base
        self.debug = debug

    def search(self, word, max_page_num):
        self.word = word
        self.directory = os.path.join(DIR, word.split(' ')[0])
        self.max_page_num = max_page_num
        self.image_urls = self._get_image_urls()
        if self.image_urls:
            self._download_images()

    def close(self):
        self.driver.quit()

    def _get_image_urls(self):
        if self.debug:
            self.driver = webdriver.Chrome()
        else:
            self.driver = webdriver.PhantomJS()
        print 'Begin to search image urls for "%s"' % self.word
        image_urls = []
        index_file_path = os.path.join(DIR, self.word + '.txt')
        if os.path.exists(index_file_path):
            print 'Loading urls from file...'
            with open(index_file_path, 'r') as f:
                for line in f.readlines():
                    image_urls.append(line.strip())
        else:
            print 'Collecting urls from pages...'
            # 连接网页
            times_to_try = 5
            for i in range(times_to_try):
                try:
                    self.driver.get(self.url_base)
                    blank = self.driver.find_element_by_id('kw')
                    blank.clear()
                    blank.send_keys(self.word)
                    self.driver.find_element_by_css_selector('input.s_btn').click()
                    break
                except Exception, e:
                    print 'Fail to search "%s" due to exception: %s' % (self.word, e)
                    if i == times_to_try - 1:
                        print 'Give up!'
                        return None
                    print 'Trying again...'
            # 爬取url
            page_count = 1
            for i in range(self.max_page_num):
                try:
                    elements = [x.find_element_by_tag_name('img') for x in self.driver.find_elements_by_class_name('imglink')]
                    for element in elements:
                        url = element.get_attribute('src')
                        if not url:
                            continue
                        image_urls.append(url)
                except Exception, e:
                    print 'Fail to collect an url due to %s' % e
                finally:
                    if i % 10 == 0 or i == self.max_page_num-1:
                        print '%d image urls collected' % len(image_urls)
                    # 若每次都模拟点击“下一页”，页面只会在某几个页面中循环，原因不详
                    # 因此只能每次模拟点击具体的页码
                    elements = self.driver.find_elements_by_class_name('pc')
                    for element in elements:
                        if element.text == str(page_count + 1):
                            element.click()
                            break
                    page_count += 1
            # 将搜集的url全部写入文件中
            with open(index_file_path, 'w') as f:
                for image_url in image_urls:
                    f.write(image_url + '\n')

        return image_urls

    def _download_images(self):
        if not os.path.exists(self.directory):
            os.mkdir(self.directory)
        print 'Begin to download images for "%s"' % self.word
        pool = Pool(processes=4)
        # 传给pool.map()的函数必须是picklable，而函数仅当在模块顶层定义时才是picklable
        pool.map(self, self.image_urls)
        print 'Totally %d images downloaded and %d discarded for "%s"' % (monitor['num_download'].value, monitor['num_discard'].value, self.word)

    def _download_single_image(self, image_url):
        file_name = os.path.join(self.directory, image_url.replace('/', ''))
        extension = os.path.splitext(file_name)[1]
        global monitor
        if extension == '.gif' or os.path.exists(file_name):
            monitor['num_discard'].value += 1
            return
        try:
            with open(file_name, 'wb') as f:
                data = requests.get(image_url, timeout=3).content
                f.write(data)
        except Exception, e:
            print 'Fail to download an image due to %s' % e
        if monitor['num_download'].value % 10 == 0:
            print '%d images downloaded' % monitor['num_download'].value
        monitor['num_download'].value += 1

    # 作为Pool.map的辅助函数
    def __call__(self, image_url):
        self._download_single_image(image_url)

url_base = "https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&pn=0&gsm=50&ct=&ic=0&lm=-1&width=0&height=0&word=word"
crawler = ImagesCrawler(url_base, debug=False)
to_search = ['acer', 'kindle', 'nike', 'benz', 'beats', 'casio']
for x in to_search:
    # 多进程的共享变量应是Value或Array类型， 且是picklable
    monitor = {}
    monitor['num_discard'] = Value('i', 0)
    monitor['num_download'] = Value('i', 0)
    crawler.search(x + u' 标志', 10)
crawler.close()