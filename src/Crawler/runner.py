# -*- coding:utf-8 -*-

from images_crawler import ImagesCrawler
from brands_crawler import BrandsCrawler
from multiprocessing import Pool

NUM_SEARCH_PAGES = 30
LOGOS_DIR = '../../data/logos'
BRANDS_DIR = '../../data/brands.txt'

NUM_PROCESSES = 4

def search(word):
    # 保证最后一定关闭浏览器
    try:
        crawler = ImagesCrawler()
        crawler.search(word, NUM_SEARCH_PAGES, LOGOS_DIR)
    except Exception, e:
        print e
    finally:
        crawler.close()
    
if __name__ == '__main__':
    brands_crawler = BrandsCrawler()
    to_search = brands_crawler.get_brands(BRANDS_DIR)[:100]
    pool = Pool(processes=NUM_PROCESSES)
    pool.map(search, to_search)
