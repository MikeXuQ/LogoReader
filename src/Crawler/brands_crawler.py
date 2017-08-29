# -*- coding:utf-8 -*-

from selenium import webdriver

class BrandsCrawler(object):
    def __init__(self, url, debug=False):
        self.url = url
        self.debug = debug

    def get_brands(self):
        self.brands = []
        if self.debug:
            self.driver = webdriver.Chrome()
        else:
            self.driver = webdriver.PhantomJS()
        self.driver.get(self.url)
        categories = [x.text for x in \
            self.driver.find_elements_by_xpath('//li[contains(@class, \'j_MenuNav\')]//a')]
        for category in categories:
            self.driver.find_element_by_name('q').send_keys(category)
            self.driver.find_element_by_xpath('//button[@type=\'submit\']').click()
            print self.driver.current_url
            self.brands += [x.title for x in \
                self.driver.find_elements_by_xpath('//ul[contains(@class, \'av-collapse\')]//a')]

if __name__ == '__main__':
    url = 'https://www.tmall.com'
    crawler = BrandsCrawler(url, debug=False)
    crawler.get_brands()