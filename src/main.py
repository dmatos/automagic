# coding=utf8

from app.crawler.tcgplayer import TCGCrawler

if __name__ == '__main__':
    crawler = TCGCrawler()
    crawler.crawl()
