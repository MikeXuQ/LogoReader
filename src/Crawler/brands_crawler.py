# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

class BrandsCrawler(object):
    def __init__(self, url, debug=False):
        self.url = url
        self.debug = debug

    def get_brands(self):
        brands = []
        if self.debug:
            self.driver = webdriver.Chrome()
        else:
            self.driver = webdriver.PhantomJS()
        self.driver.get(self.url)
        category = self.driver.find_element_by_class_name("nav-line-2")
        hover = ActionChains(self.driver).move_to_element(category)
        hover.perform()

        panels = self.driver.find_elements_by_class_name('nav-hasPanel')
        # 从第4个panel开始遍历，首先收集每个分类的链接
        category_links = [link.get_attribute('href') \
            for i in range(3, len(panels)) \
                for link in panels[i].find_elements_by_tag_name('a')]
        print 'url', category_links
        for category_link in category_links:
            self.driver.get(category_link)
            tmp_element = [x for x in self.driver.find_elements_by_tag_name('h3') if x.text == u'品牌'][0]
            brands += [x.text for x in\
                tmp_element.find_elements_by_xpath('following-sibling::ul//a')]
            print brands

if __name__ == '__main__':
    url = 'https://www.amazon.cn'
    crawler = BrandsCrawler(url, debug=True)
    crawler.get_brands()