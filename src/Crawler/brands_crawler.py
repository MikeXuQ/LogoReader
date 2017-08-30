# -*- coding:utf-8 -*-

import requests
from lxml import etree
import os

class BrandsCrawler(object):
    def __init__(self):
        self.category_url = 'https://www.jd.com'
        self.search_url_base = 'https://search.jd.com/Search?enc=utf-8&keyword='

    def get_brands(self, file_path):
        brands = []
        if os.path.exists(file_path):
            print 'Getting brands from file...'
            with open(file_path, 'r') as f:
                for line in f.readlines():
                    brands.append(line.strip())
        else:
            print 'Getting brands from pages...'
            categories = self._get_categories()
            with open(file_path, 'w') as f:
                for category in categories:
                    print 'Searching brands for "%s"...' % category
                    try:
                        page = requests.get(self.search_url_base + category, timeout=8).content
                        html = etree.HTML(page)
                        to_add = [x.encode('utf-8') for x in \
                            html.xpath('//div[contains(@class, \'s-brand\')]//ul[contains(@class, \'v-fixed\')]//a/@title')]
                        brands += to_add
                        for brand in to_add:
                            f.write(brand + '\n')
                    except Exception, e:
                        print 'Fail to get brands of "%s" due to %s' % (category, e)

        return brands

    def _get_categories(self):
        print 'Collecting categories...'
        page = requests.get(self.category_url).content
        html = etree.HTML(page)
        return [x.encode('utf-8') for x in \
            html.xpath('//li[contains(@class, \'cate_menu_item\')]//a/text()')]
