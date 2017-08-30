# -*- coding:utf-8 -*-

import requests
from lxml import etree
import os

class BrandsCrawler(object):
    def __init__(self):
        self.category_url = 'https://www.jd.com'
        self.search_url_base = 'https://search.jd.com/Search?enc=utf-8&keyword='

    def get_brands(self, file_path):
        # 注意需保证返回的字符为unicode编码
        brands = []
        if os.path.exists(file_path):
            print 'Getting brands from file...'
            with open(file_path, 'r') as f:
                for line in f.readlines():
                    brands.append(line.strip().decode('utf-8'))
        else:
            print 'Getting brands from pages...'
            categories = self._get_categories()
            for category in categories:
                print 'Searching brands for "%s"...' % category
                times_to_try = 3
                for i in range(times_to_try):
                    try:
                        page = requests.get(self.search_url_base + category, timeout=5).content
                        html = etree.HTML(page)
                        brands += [x for x in \
                            html.xpath('//div[contains(@class, \'s-brand\')]//ul[contains(@class, \'v-fixed\')]//a/@title')]
                    except Exception, e:
                        if i == times_to_try-1:
                            print 'Fail to get brands of "%s" due to %s' % (category, e)
            with open(file_path, 'w') as f:
                for brand in brands:
                    # 需将unicode转化为utf-8才可保存至文件
                    f.write(brand.encode('utf-8') + '\n')

        return brands

    def _get_categories(self):
        print 'Collecting categories...'
        page = requests.get(self.category_url).content
        html = etree.HTML(page)
        return [x.encode('utf-8') for x in \
            html.xpath('//li[contains(@class, \'cate_menu_item\')]//a/text()')]
