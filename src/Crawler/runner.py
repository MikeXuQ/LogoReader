from images_crawler import ImagesCrawler
from brands_crawler import BrandsCrawler
from multiprocessing import Pool

NUM_SEARCH_PAGES = 3
LOGOS_DIR = '../../data/logos'
BRANDS_DIR = '../../data/brands.txt'

NUM_PROCESSES = 4

def search(word):
    crawler = ImagesCrawler()
    crawler.search(word, NUM_SEARCH_PAGES, LOGOS_DIR)
    crawler.close()
    
if __name__ == '__main__':
    brands_crawler = BrandsCrawler()
    to_search = brands_crawler.get_brands(BRANDS_DIR)
    pool = Pool(processes=NUM_PROCESSES)
    pool.map(search, to_search)
