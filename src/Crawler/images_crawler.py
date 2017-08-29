# -*- coding:utf-8 -*-

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from multiprocessing import Pool, Value
import os

class ImagesCrawler(object):
    def __init__(self, url_base, debug=False):
        self.url_base = url_base
        self.debug = debug

    def search(self, word, max_page_num, files_dir):
        self.word = word
        self.files_dir = files_dir
        self.subdir = os.path.join(self.files_dir, word.split(' ')[0])
        if not os.path.exists(self.subdir):
            os.makedirs(self.subdir)
        self.max_page_num = max_page_num
        self._get_image_urls()
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
        self.image_urls = []
        index_file_path = os.path.join(self.files_dir, self.word + '.txt')
        if os.path.exists(index_file_path):
            self._load_urls_from_file(index_file_path)
        else:
            self._collect_urls_from_pages(index_file_path)

    def _load_urls_from_file(self, index_file_path):
        print 'Loading urls from file for "%s"...' % self.word
        with open(index_file_path, 'r') as f:
            for line in f.readlines():
                self.image_urls.append(line.strip())

    def _collect_urls_from_pages(self, index_file_path):
        print 'Collecting urls from pages for "%s"...' % self.word

        if not self._connect_to_pages():
            self.image_urls = None
            return

        # 爬取url
        page_count = 1
        for i in range(self.max_page_num):
            try:
                elements = [x.find_element_by_tag_name('img') for x in self.driver.find_elements_by_class_name('imglink')]
                for element in elements:
                    url = element.get_attribute('src')
                    if not url:
                        continue
                    self.image_urls.append(url)
            except Exception, e:
                print 'Fail to collect an image url of "%s" due to %s' % (self.word, e)
            finally:
                if i % 10 == 0 or i == self.max_page_num-1:
                    print '%d image urls of "%s" collected' % (len(self.image_urls), self.word)
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
            for image_url in self.image_urls:
                f.write(image_url + '\n')

    def _connect_to_pages(self):
        # 连接网页，返回True表示连接成功
        times_to_try = 5
        for i in range(times_to_try):
            try:
                self.driver.get(self.url_base)
                blank = self.driver.find_element_by_id('kw')
                blank.clear()
                blank.send_keys(self.word)
                self.driver.find_element_by_css_selector('input.s_btn').click()
                return True
            except Exception, e:
                print 'Fail to search "%s" due to exception: %s' % (self.word, e)
                if i == times_to_try - 1:
                    print 'Give up searching "%s"!' % self.word
                    return False
                print 'Trying to search "%s" again...' % self.word

    def _download_images(self):
        print 'Begin to download images for "%s"' % self.word
        self.num_discard = 0
        self.num_download = 0
        for image_url in self.image_urls:
            self._download_single_image(image_url)
        print 'Totally %d images downloaded and %d discarded for "%s"' % (self.num_download, self.num_discard, self.word)

    def _download_single_image(self, image_url):
        file_name = os.path.join(self.subdir, image_url.replace('/', ''))
        extension = os.path.splitext(file_name)[1]
        if extension == '.gif' or os.path.exists(file_name):
            self.num_discard += 1
            return
        try:
            with open(file_name, 'wb') as f:
                data = requests.get(image_url, timeout=3).content
                f.write(data)
        except Exception, e:
            print 'Fail to download an image of "%s" due to %s' % (self.word, e)

        if self.num_download % 10 == 0:
            print '%d images of "%s" downloaded' % (self.num_download, self.word)
        self.num_download += 1
    