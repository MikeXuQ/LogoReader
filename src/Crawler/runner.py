from images_crawler import ImagesCrawler
from brands_crawler import BrandsCrawler
from multiprocessing import Pool

URL_BASE = "https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&pn=0&gsm=50&ct=&ic=0&lm=-1&width=0&height=0&word=word"
NUM_SEARCH_PAGES = 3
LOGOS_DIR = '../../data/logos'
BRANDS_DIR = '../../data/brands'

NUM_PROCESSES = 4

def search(word):
    crawler = ImagesCrawler(URL_BASE, debug=False)
    crawler.search(word, NUM_SEARCH_PAGES, LOGOS_DIR)
    crawler.close()
	
if __name__ == '__main__':
	brands_crawler = BrandsCrawler()
    to_search = brands_crawler.get_brands(BRANDS_DIR)
    pool = Pool(processes=NUM_PROCESSES)
    pool.map(search, to_search)