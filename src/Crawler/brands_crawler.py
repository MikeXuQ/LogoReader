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
            self.driver.find_elements_by_xpath('//li[contains(@class, \'cate_menu_item\')]//a')]
        for category in categories:
            search_blank = self.driver.find_element_by_id('key')
            search_blank.clear()
            search_blank.send_keys(category)
            self.driver.find_element_by_xpath('//button[contains(@class, \'button\')]').click()
            print 'Searching category "%s"' % category.encode('utf-8')
            # 处理特殊页面导致的异常
            try:
                to_add = [x.get_attribute('title').encode('utf-8') for x in \
                    self.driver.find_elements_by_xpath('//div[contains(@class, \'s-brand\')]//ul[contains(@class, \'v-fixed\')]//a')]
                print 'Brands to add:\n', to_add
                self.brands += to_add
            except Exception, e:
                print 'Fail to collect brands of "%s" due to %s' % (category, e)

        self.driver.close()

if __name__ == '__main__':
    url = 'https://www.jd.com'
    crawler = BrandsCrawler(url, debug=False)
    crawler.get_brands()