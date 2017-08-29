from images_crawler import ImagesCrawler
from multiprocessing import Pool

URL_BASE = "https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&pn=0&gsm=50&ct=&ic=0&lm=-1&width=0&height=0&word=word"
NUM_SEARCH_PAGES = 3
LOGOS_DIR = '../../data/logos'

NUM_PROCESSES = 4

def search(word):
    crawler = ImagesCrawler(URL_BASE, debug=False)
    crawler.search(word, NUM_SEARCH_PAGES, LOGOS_DIR)
    crawler.close()
	
if __name__ == '__main__':
    to_search = ['acer', 'kindle', 'nike', 'benz', 'beats', 'casio']
    pool = Pool(processes=NUM_PROCESSES)
    pool.map(search, to_search)